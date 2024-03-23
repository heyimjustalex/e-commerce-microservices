
from pymongo.database import Database
from typing import Any, Callable
from pymongo.collection import Collection
import pytest
from pytest import MonkeyPatch  # Correct import
from fastapi.testclient import TestClient
from mongomock import MongoClient as MockMongoClient
from typing import Union
import os

from app.app import app
client = TestClient(app)
API_AUTHENTICATION_PREFIX:str = os.getenv('API_AUTHENTICATION_PREFIX','/api/auth')

@pytest.fixture()
def inmemory_database_creation_function() -> Callable[[], Database[Any]]:
    def db_creation() -> Database[Any]:
        client = MockMongoClient()  
        db: Database[Any] = client['shop']
        collection: Collection[Any] = db['users']
        collection.insert_one({'email': 'aaa@aaa.com',    "role":"user", 'password_hash': '9c520caf74cff9b9a891be3694b20b3586ceb17f2891ceb1d098709c1e0969a3'})
        collection.insert_one({'email': 'bbb@bbb.com',    "role":"user", 'password_hash': '77cd27bc3de668c18ed6be5f5c2909ffdacdf67705c30d132003ad5a89085deb'})
        collection.insert_one({'email': 'a64cb39621534d604e02@d9fc5f.com',  "role":"user", 'password_hash': '27aca3b16db6ef313dd6ff97d36c2fa9608af08f48a7e2b1da1527a234f008fd'})
        return db 
    return db_creation
