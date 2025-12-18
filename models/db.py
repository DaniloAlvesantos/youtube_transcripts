from pymongo import MongoClient

class DB:
    _uri = ""
    def __init__(self):
        self._client = MongoClient(self._uri)
        self._db = self._client.get_database("")

    def get_collection(self, collection):
        return self._db.get_collection(collection)
    
    @property
    def db(self):
        return self._db

    @property
    def client(self):
        return self._client
    