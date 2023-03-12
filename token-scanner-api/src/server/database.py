# -*- encoding: utf-8 -*-
# server/database.py
# This class implements the database connection.


from pymongo import MongoClient




client = MongoClient(MONGO_DETAILS)

database = client.balances

collection = database.get_collection("balances_fuckkk")


print(database.list_collection_names())


def wallet_helper(item) -> dict:
    return {
        "wallet": item["wallet"],
    }


from bson.objectid import ObjectId

async def retrieve_students():
    bals = collection.find()

    res = []
    counter = 0
    for i in bals:
        res.append(wallet_helper(i))
        if counter > 2:
            break
        counter += 1

    return res


def balancer_helper(item) -> dict:
    return {
        "wallet": item["wallet"],
        "balance": item["balance"],
    }


# Retrieve a student with a matching ID
async def retrieve_balance(wallet: str) -> dict:
    balance = collection.find_one({"wallet": wallet})
    if balance:
        return balancer_helper(balance)

async def retrieve_top_balances():
    pass

async def retrieve_holder_weekly_change(address: str):
    pass