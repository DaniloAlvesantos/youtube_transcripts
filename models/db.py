from typing import Collection
from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId

class DB:
    """
    MONGODB MANAGER CLASS
    """

    _uri: str = "mongodb://localhost:27017"
    def __init__(self):
        self._client = MongoClient(self._uri)
        self._db = self._client.get_database("youtube")

    def get_collection(self, collection: str) -> Collection:
        return self._db.get_collection(collection)

    def format_to_id(self, id: str) -> ObjectId:
        return ObjectId(id)

    @property
    def db(self):
        return self._db

    @property
    def client(self) -> MongoClient:
        return self._client
