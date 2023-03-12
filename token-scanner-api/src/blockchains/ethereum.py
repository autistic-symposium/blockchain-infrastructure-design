# -*- encoding: utf-8 -*-
# blockchains/ethereum.py
# This class implements a blockchain indexer for Ethereum.

import time
import datetime

from web3 import Web3
from decimal import Decimal
from collections import defaultdict
from web3.exceptions import BlockNotFound
from web3.providers.rpc import HTTPProvider

from src.utils.arithmetics import convert_hex_to_int
from src.utils.os_utils import send_rpc_request, exit_with_error, create_result_file, \
                               set_output, open_json, load_config, save_output, log_info


class TokenIndexer:
    
    def __init__(self):

        self.env_vars = load_config()
        self.web3 = self._set_web3_object()

        # contract parameters
        self.contract_address = self.env_vars['TOKEN_CONTRACT']
        self.contract_abi = self._set_contract_abi()
        self.contract_object = self.web3.eth.contract(abi=self.contract_abi)

        # indexing parameters
        self.provider_url = self.env_vars['RPC_PROVIDER_URL']
        self.max_retries = int(self.env_vars['MAX_RETRIES'])
        self.size_chunks_next = int(self.env_vars['SIZE_CHUNK_NEXT'])
        self.decimal = self._set_decimal()

        # results parameters
        self.result_data = {}
        self.result_filepath = self._set_result_destination()


    ###########################################
    #     Private methods: setters            #
    ###########################################

    def _set_web3_object(self) -> None:
        """Set web3 object from RPC provider."""

        rpc_provider = HTTPProvider(self.env_vars['RPC_PROVIDER_URL'])
        rpc_provider.middlewares.clear()
        return Web3(rpc_provider)
    
    def _set_decimal(self) -> None:
        """Set token contracts decimal."""

        return Decimal('10') ** Decimal(f'-{self.env_vars["TOKEN_DECIMALS"]}')

    def _is_connected(self) -> bool:
        """Check if the node is connected to the network."""

        if not self.web3.isConnected():
            exit_with_error('Cannot connect to the node. Exiting.')

    def _set_contract_abi(self) -> None:
        """Set contract ABI."""

        try:
            return open_json(self.env_vars['TOKEN_CONTRACT_ABI'])
        except Exception as e:
            exit_with_error(f'Cannot parse contract ABI: {e}. Exiting.')

    def _set_result_destination(self) -> None:
        """Set result destination."""

        this_result_file = create_result_file("raw_data")
        return set_output(this_result_file, self.env_vars)


    ###########################################
    #     Private methods: logic              #
    ###########################################

    def _get_block_timestamp(self, block_number) -> int:
        """Get the timestamp of a given block."""

        try:
            block_timestamp = self.web3.eth.getBlock(block_number)['timestamp']
            return int(datetime.datetime.utcfromtimestamp(block_timestamp))
        except (BlockNotFound, ValueError):
            return None
        
    def _get_logs(self, from_block: int, to_block: int) -> list:
        """Get logs from a given address between two blocks,"""

        # keccak256('Transfer(address,address,uint256)')
        topic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

        # https://docs.infura.io/infura/networks/ethereum/json-rpc-methods/eth_getlogs
        method = 'eth_getLogs'
        
        return send_rpc_request(self.provider_url, method,
                        [{'address': self.contract_address, 
                        'fromBlock': from_block,
                        'toBlock': to_block, 
                        'topics': [topic]
                        }])

    def _get_last_block_number(self) -> int:
        """
            Get the last block number with the eth_blockNumber method.
            https://docs.infura.io/infura/networks/ethereum/json-rpc-methods/eth_blocknumber
        """
        
        method = 'eth_blockNumber'
        return convert_hex_to_int(send_rpc_request(self.provider_url, method))

    def _process_logs(self, logs: list) -> dict:
        """Process the logs and return a dictionary with the results."""
        
        log_info(f'Processing {len(logs)} logs...')
        processed_logs =  defaultdict()

        try:
            for log in logs:
                processed_logs[log['transactionHash']] = {}
                processed_logs[log['transactionHash']]['blockNumber'] = convert_hex_to_int(log['blockNumber'])
                processed_logs[log['transactionHash']]['from'] = '0x' + log['topics'][1][26:]
                processed_logs[log['transactionHash']]['to'] = '0x' + log['topics'][2][26:]
                processed_logs[log['transactionHash']]['amount'] = float(Decimal(convert_hex_to_int(log['data'])) * self.decimal)
        except KeyError as e:
            print(f'Error processing logs: {e}')
            
        return processed_logs


    ###########################
    #   Public methods        #
    ###########################

    def get_transfer_logs_chunks(self, from_block=None, to_block=None) -> list:
        """Get transfer logs from a given address between two blocks by small chunks"""
        
        logs = []
        from_block = from_block or 1
        to_block = to_block or self._get_last_block_number()

        log_info(f'Indexing transfer events between blocks {from_block} and {to_block}...')
        for block in range(from_block, to_block, self.size_chunks_next):
            attempt = 0
            while attempt < self.max_retries:
                last_block = block + self.size_chunks_next
                print(f'loading blocks {block} to {last_block}')
                try:
                    this_logs = self._get_logs(hex(block), hex(last_block))
                    if this_logs:
                        log_info(f'Found {len(this_logs)} transfer events between blocks {block} and {last_block}.')
                        logs += this_logs
                    break
                except Exception:
                    attempt += 1
        
        self.result_data = self._process_logs(logs)

    def run(self):
        """Run the indexer."""

        start_time = time.time()
        self.get_transfer_logs_chunks()

        delta_time = time.time() - start_time
        log_info(f'{len(self.result_data)} transfer events were indexed on {round(delta_time, 3)} seconds.')

        save_output(self.result_filepath, self.result_data)

