# -*- encoding: utf-8 -*-
# server/api.py
# This class implements the API server.

from fastapi import FastAPI
from pymongo import MongoClient

from src.utils import os_utils
from src.server.routes import router 


app = FastAPI()
app.include_router(router)

env_vars = os_utils.load_config()
url = env_vars['MONGODB_URL']
db_name = env_vars['MONGODB_DB_NAME']

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(url)
    app.database = app.mongodb_client[db_name]
    os_utils.log_info("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
