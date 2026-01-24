import os
from pymongo import MongoClient
from bson import ObjectId

class DB:
    """
    MONGODB MANAGER CLASS
    """

    def __init__(self):
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/youtube")
        self._client = MongoClient(uri)
        self._db = self._client.get_database()

    def get_collection(self, collection):
        return self._db.get_collection(collection)

    def format_to_id(self, id: str) -> ObjectId:
        return ObjectId(id)

    @property
    def db(self):
        return self._db

    @property
    def client(self):
        return self._client
