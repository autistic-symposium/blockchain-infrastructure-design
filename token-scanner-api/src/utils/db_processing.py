# -*- encoding: utf-8 -*-
# utils/db_processing.py
# Furnish the database with data. This should be run once.

import pymongo
import src.utils.os_utils as os_utils


def format_and_load_data(filepath):
    """Load and parse data prior being ingested into the database."""

    data = os_utils.open_json(filepath) 
    result = []

    for wallet, balance in data.items():
        result.append({"wallet": wallet, "balance": balance})

    return result


def run_db_processing(filepath, env_vars):

    #################################
    # Connect to database via client
    #################################
    url = env_vars['MONGODB_URL']
    db_name = env_vars['MONGODB_DB_NAME']
    collection = env_vars['MONGODB_COLLECTION_NAME']
    
    client = pymongo.MongoClient(url)

    with client:
        ##############################
        # Create database for balances
        ##############################
        database = client[db_name]

        ################################
        # Create collection for balances
        # (make sure it's empty first)
        ################################
        wallet_collection = database[collection]
        wallet_collection.drop()

        ##############################
        # Load wallet balances into db
        ##############################
        data = format_and_load_data(filepath)
        wallet_collection.insert_many(data)

        os_utils.log_info(f'Inserted {len(data)} records into database.')
        os_utils.log_info(f'Number of records in database: {wallet_collection.count_documents({})}')
        os_utils.log_info(f'Example of record: {wallet_collection.find_one()}')
