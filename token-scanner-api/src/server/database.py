# -*- encoding: utf-8 -*-
# server/database.py
# This class implements the database connection.


import pymongo 
import src.utils.os_utils as os_utils


############################################
#     Private methods: database            #
############################################

def _get_db_collection():
    """Connect to the database."""

    env_vars = os_utils.load_config()

    url = env_vars['MONGODB_URL']
    db_name = env_vars['MONGODB_DB_NAME']
    collection = env_vars['MONGODB_COLLECTION_NAME']

    client = pymongo.MongoClient(url)
    database = client[db_name]
    return database[collection]


def _wallet_helper(item) -> dict:
    return {
        "wallet": item["wallet"],
    }


def _balancer_helper(item) -> dict:
    return {
        "wallet": item["wallet"],
        "balance": item["balance"],
    }


############################################
#     Public methods: database             #
############################################

async def retrieve_top_balances() -> list:
    """Retrieve top balances from the database."""

    top_number = 100
    collection = _get_db_collection()
    top_balances = collection.find()#.sort({"balance"}, pymongo.DESCENDING).limit(top_number)

    result = []
    counter = 0
    
    for balance in top_balances:
        result.append(_wallet_helper(balance))
        if counter > top_number:
            break
        counter += 1

    return top_balances


async def retrieve_balance(wallet: str) -> dict:
    """Retrieve balance from the database."""

    collection = _get_db_collection()
    balance = collection.find_one({"wallet": wallet})

    if balance:
        return _balancer_helper(balance)
    else:
        return {}



async def retrieve_holder_weekly_change(address: str) -> int:
    """Retrieve weekly change of a given address."""

    collection = _get_db_collection()
    # todo
    # get today time
    # get last week time
    # find block last week
    # get balance of address in block last week
    # get balance of address in block today
    # calculate difference and percentage
    pass
