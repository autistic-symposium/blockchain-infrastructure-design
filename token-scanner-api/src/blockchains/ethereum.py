# -*- encoding: utf-8 -*-
# blockchains/ethereum.py
# This class implements a blockchain indexer for Ethereum.

import time
import datetime

from web3 import Web3
from web3.exceptions import BlockNotFound
from web3.providers.rpc import HTTPProvider
from web3._utils.filters import construct_event_filter_params

import src.utils.os_utils as os_utils
from src.utils.arithmetics import wei_to_eth, to_decimal


class TokenIndexer:
    
    def __init__(self, indexing_type = "address"):

        self.env_vars = os_utils.load_config()
        self.web3 = self._set_web3_object()
        
        if not self._is_connected():
            os_utils.exit_with_error('Cannot connect to the node. Exiting.')

        # contract parameters
        self.contract_address = self.env_vars['TOKEN_CONTRACT']
        self.contract_abi = self._set_contract_abi()
        self.contract_object = self.web3.eth.contract(abi=self.contract_abi)
        self.events = self.contract_object.events.Transfer

        # indexing parameters
        self.indexing_type = self._set_indexing_type(indexing_type)
        self.max_retries = int(self.env_vars['MAX_RETRIES'])
        self.retries_timeout = float(self.env_vars['RETRIES_TIMEOUT'])
        self.size_chunks_next = float(self.env_vars['SIZE_CHUNK_NEXT'])

        # results parameters
        self.result_data = {}
        self.result_filepath = self._set_result_destination()


    ###########################################
    #     Private methods: setters            #
    ###########################################

    def _is_connected(self) -> bool:
        """Check if the node is connected to the network."""

        return self.web3.isConnected()

    def _set_web3_object(self) -> None:
        """Set web3 object from RPC provider."""

        rpc_provider = HTTPProvider(self.env_vars['RPC_PROVIDER_URL'])
        rpc_provider.middlewares.clear()
        return Web3(rpc_provider)

    def _set_result_destination(self) -> None:
        """Set result destination."""

        this_result_file = os_utils.create_result_file("raw_data")
        return os_utils.set_output(this_result_file, self.env_vars)
    
    def _set_contract_abi(self) -> None:
        """Set contract ABI."""

        try:
            return os_utils.open_json(self.env_vars['TOKEN_CONTRACT_ABI'])
        except Exception as e:
            os_utils.exit_with_error(f'Cannot parse contract ABI: {e}. Exiting.')

    def _set_indexing_type(self, indexing_type: str) -> None:
        """Set filter for indexing."""

        if indexing_type == "address":
            return {indexing_type: self.contract_address}
            
        else:
             os_utils.exit_with_error(f'Indexing type {indexing_type} is not implemented yet. Exiting.')


    ###########################################
    #     Private methods: logic              #
    ###########################################

    def _get_end_block(self, start_block) -> int:
        """Get the last block to index."""

        end_block = self.web3.eth.blockNumber - 1
    
        if start_block > end_block:
            os_utils.exit_with_error(f'Cannot start from block {start_block} and end at block {end_block}. Exiting.')

        return end_block

    def _get_block_timestamp(self, block_number) -> int:
        """Get the timestamp of a given block."""

        try:
            block_timestamp = self.web3.eth.getBlock(block_number)['timestamp']
            return int(datetime.datetime.utcfromtimestamp(block_timestamp))
        except (BlockNotFound, ValueError):
            return None
        
    def _fetch_events(self, start_block, end_block) -> dict:
        """Fetch events from a range of blocks."""

        # https://github.com/ethereum/web3.py/blob/master/web3/_utils/filters.py
        _, event_filter = construct_event_filter_params(self.contract_abi,
                                                        self.web3.codec,
                                                        address=self.contract_address,
                                                        argument_filters=self.indexing_type,
                                                        fromBlock=start_block,
                                                        toBlock=end_block)
        filter_logs = self.web3.eth.get_logs(event_filter)
        return [self._get_event_data(self.web3.codec, self.contract_abi, event) for event in filter_logs]

    def _web3_retry_call(self, start_block, end_block) -> None:
        """Handle eth_getLogs multiple reuests by retrying."""

        retry = 0
        while retry < self.max_retries - 1:
            try:
                return end_block, self._fetch_events(start_block, end_block)
            
            except Exception as e:
                os_utils.log_error(f'Failed to index events for blocks range {start_block} to {end_block}: {e}')
                end_block = start_block + ((end_block - start_block) // 2)
                time.sleep(self.retries_timeout)
                retry += 1

    def _run_indexer_by_chunk(self, start_block, end_block_for_chunk) -> (int, dict):
        """Run the indexer for each chunk."""

        this_results = []
        this_end_block, events = self._web3_retry_call(start_block, end_block_for_chunk)

        for events in events:
            transfer = {
                "from": events["args"]["from"],
                "to": events["args"]["to"],
                "value": str(to_decimal(wei_to_eth(events["args"]["to"],))),
            }
            this_results.append(transfer)
        
        return this_end_block, this_results
    
    def _run_indexer(self, start_block=None, end_block=None) -> None:

        # set up the indexer
        results = {}
        start_block = start_block or 0
        end_block = end_block or self._get_end_block(start_block)

        # start the indexer loop
        while start_block <= end_block:

            end_block_for_chunk = int(start_block + self.size_chunks_next)
            os_utils.log_info(f'Indexing transfers for blocks: {start_block} - {end_block_for_chunk}')    

            # scan chunk   
            this_block_end, this_results = self._run_indexer_by_chunk(start_block, end_block_for_chunk)

            # update indexer parameters
            results += this_results
            start_block = this_block_end + 1

        self.result_data = results


    ###########################
    #   Public methods        #
    ###########################

    def run(self):
        """Run the indexer."""

        start_time = time.time()
        self._run_indexer()

        print(self.result_data)
        import sys
        sys.exit()
        delta_time = time.time() - start_time
        os_utils.log_info(f'{len(self.result_data)} transfer events were indexed on {delta_time} seconds.')

        os_utils.save_output(self.result_filepath, self.result_data)
        os_utils.log_info(f'Results were saved at {self.result_filepath}.')
