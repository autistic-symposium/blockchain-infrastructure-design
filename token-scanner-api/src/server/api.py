from fastapi import FastAPI
from routes import router 


app = FastAPI()

app.include_router(router)


from pymongo import MongoClient


url = "mongodb://localhost:27017/"
DB_NAME = "balances"

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(url)
    app.database = app.mongodb_client[DB_NAME]

    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()