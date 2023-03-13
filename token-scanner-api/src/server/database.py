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


def _balancer_helper(item) -> dict:
    return {
        "wallet": item["wallet"],
        "balance": item["balance"],
    }


############################################
#     Public methods: database             #
############################################

async def retrieve_top_balances(top_number=None) -> list:
    """Retrieve top balances from the database."""

    top_number = top_number or 100
    collection = _get_db_collection()
    top_balances = collection.find().sort("balance", -1).limit(top_number)

    result = []
    for item in top_balances:
        result.append({
            "wallet": item["wallet"],
            "balance": item["balance"],
        })

    return result


async def retrieve_balance(wallet: str) -> dict:
    """Retrieve balance from the database."""

    collection = _get_db_collection()
    balance = collection.find_one({"wallet": wallet})

    if balance:
        return _balancer_helper(balance)
    else:
        return {}

