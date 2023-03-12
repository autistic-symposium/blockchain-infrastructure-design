#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# Entry point for ethereum-token-api.

import uvicorn
import argparse

from src.utils.os_utils import load_config
from src.utils.db_processing import populate_db
from src.blockchains.ethereum import TokenIndexer
from src.utils.vercel_utils import upload_to_vercel
from src.utils.test_api import fetch_token_balance as f 
from src.utils.data_processing import run_data_processing


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='🪙 Token indexer and API.')
  
    parser.add_argument('-e', dest='indexer',  action='store_true', \
                        help="Retrieve historical transfer events data on Ethereum. \
                        Example: indexer -e")
    parser.add_argument('-p', dest='process', nargs=1,
                        help="Process historical transfer events data. \
                        Example: indexer -p <json data file>")
    parser.add_argument('-d', dest='db', nargs=1,
                        help="Populate local db with processed event data. \
                        Example: indexer -d <json data file>")

    parser.add_argument('-a', dest='api', action='store_true',
                        help="Run the event scanner api locally. \
                        Example: indexer -a")
    parser.add_argument('-c', dest='vercel', action='store_true',
                        help="Deploy event scanner to Vercel. \
                        Example: indexer -c")
    
    parser.add_argument('-b', dest='balance', nargs=1,
                        help="Fetch token balance for a given wallet. \
                        Example: indexer -b <wallet address>")
    parser.add_argument('-t', dest='top', nargs=1,
                        help="Fetch top token holders. \
                        Example: indexer -t <number of holders>")
    parser.add_argument('-g', dest='change', nargs=1,
                        help="Fetch weekly balance change for a given wallet. \
                        Example: indexer -g <wallet address>")
    return parser


def run() -> None:
    """Entry point for this module."""

    load_config()
    parser = run_menu()
    args = parser.parse_args()

    #############################
    # Run historical data indexer
    #############################
    if args.indexer:
      indexer = TokenIndexer()
      indexer.run()
    elif args.process:
      run_data_processing(args.process[0])
    elif args.db:
      populate_db(args.db[0])

    #############################
    # Run deployment tools
    #############################
    elif args.api:
      uvicorn.run("src.server.api:app", host="0.0.0.0", port=8000, reload=True)
    elif args.vercel:
      upload_to_vercel()

    #############################
    # Run api tests
    #############################
    elif args.balance:
      f.fetch_token_balance(args.balance[0])
    elif args.top:
      f.fetch_top_holders(args.top[0])
    elif args.change:
      f.fetch_change(args.change[0])


    else:
      parser.print_help()


if __name__ == "__main__":
    run()