# -*- encoding: utf-8 -*-
# server/database.py
# This class implements the database connection.


import pymongo 
from src.utils import os_utils


############################################
#     Private methods: database            #
############################################

def _get_db_collection(env_vars):
    """Connect to the database."""

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

async def retrieve_top_balances(top_number: int, env_vars: dict) -> list:
    """Retrieve top balances from the database."""

    collection = _get_db_collection(env_vars)
    # todo: need to sort? how to optimzie to not return all?
    # something like for post in posts.find({"date": {"$lt": d}}).sort("author"):
    top_balances = collection.find()

    result = []
    counter = 0
    
    for balance in top_balances:
        result.append(_wallet_helper(balance))
        if counter > top_number:
            break
        counter += 1

    return result


async def retrieve_balance(wallet: str, env_vars: dict) -> dict:
    """Retrieve balance from the database."""

    collection = _get_db_collection(env_vars)
    balance = collection.find_one({"wallet": wallet})

    if balance:
        return _balancer_helper(balance)
    else:
        return {}


async def retrieve_holder_weekly_change(address: str, env_vars: dict) -> int:
    """Retrieve weekly change of a given address."""

    collection = _get_db_collection(env_vars)
    # todo
    # get today time
    # get last week time
    # find block last week
    # get balance of address in block last week
    # get balance of address in block today
    # calculate difference and percentage
    pass
