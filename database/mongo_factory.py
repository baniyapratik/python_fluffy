from pymongo import MongoClient

MONGO_DB_URI = "mongodb://localhost:27017"

class MongoFactory:

    def __init__(self):
        self.init_app()

    def init_app(self):
        self._client = MongoClient(MONGO_DB_URI)

    @property
    def db(self):
        return self._client

    def close(self):
        try:
            self._client.close()
        except Exception:
            pass