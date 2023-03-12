# -*- encoding: utf-8 -*-
# utils/furnish_db.py
# Furnish the database with data.

import pymongo
import src.utils.os_utils as os_utils

def run():

    url = "mongodb://localhost:27017/"

    client = pymongo.MongoClient(url)
    db = client.test
    database_name = client["balances"]
    collection_name = database_name["balances"]


    filename = "./balance.json"
    data = os_utils.open_json(filename) 


    result = []
    for wallet, balance in data.items():
        result.append({"wallet": wallet, "balance": balance})

    collection_name.insert_many(result)

def populate_db():
    pass