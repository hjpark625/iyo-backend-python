import os
from pymongo import MongoClient, database
from dotenv import load_dotenv

load_dotenv()


class Database:
    client: MongoClient
    db: database.Database
    db_name: str
    table_name: str

    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[db_name]

    def get_collection(self):
        return self.db[self.table_name]

    def close(self):
        self.client.close()
