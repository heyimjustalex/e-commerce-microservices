
from pymongo.database import Database
from typing import Any, Callable
from pymongo.collection import Collection
import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient as MockMongoClient
import os
from bson.objectid import ObjectId
from app.app import app
import mock
client = TestClient(app)
API_PRODUCT_PREFIX:str = os.getenv('API_PRODUCT_PREFIX','/api')

envs: dict[str, str] = {
    'JWT_ACCESS_TOKEN_SECRET_KEY': 'accesstokenkey',
    'JWT_REFRESH_TOKEN_SECRET_KEY': "refreshtokenkey",
    'JWT_ACCESS_TOKEN_EXPIRE_MINUTES': '10080',
    'JWT_TOKEN_ALG': 'HS256',
    'JWT_REFRESH_TOKEN_EXPIRE_MINUTES': '30',


}
    
class AIOKafkaProducerMock:
    def send(self, topic, object):
        pass

class MessageProducerMock:
    isStarted = False 

    @classmethod
    async def _create_producer(cls):
        return AIOKafkaProducerMock()

    @classmethod   
    async def get_producer(cls): 
        if not cls.isStarted:
            cls._producer: AIOKafkaProducerMock = await cls._create_producer()
            cls.isStarted = True
        return cls._producer


class SessionMock:
    def start_transaction(self):
        pass

@pytest.fixture()
def client_creation_function() -> Callable[[], MockMongoClient]:
    def get_client() -> MockMongoClient:
        client = MockMongoClient() 
        # this does not work for some reason 
        with mock.patch.object(client, 'start_session') as mock_start_session:
            # Set up the mock behavior
            mock_session = mock_start_session.return_value
            mock_session.__enter__.return_value = SessionMock()

            # Call the function or code that uses MongoClient.start_session()
            session = client.start_session()

            # Assertion to verify if the mocked session is returned
            print(session)
        return client
    return get_client

@pytest.fixture()
def inmemory_database_creation_function() -> Callable[[], Database[Any]]:
    def db_creation() -> Database[Any]:
        client = MockMongoClient()  
        db: Database[Any] = client['shop']
        
        products: Collection[Any] = db['products']
        categories : Collection[Any] = db['categories']

        categories.insert_many([  
            {
                '_id': ObjectId("21fefe4a1cad4140785928a4"),
                'name': "electronics",
            },
            {
                '_id': ObjectId("22fefe4a1cad4140785928a4"),  
                'name': "kitchen",
            },
            {
                '_id': ObjectId("23fefe4a1cad4140785928a4"),
                'name': "furniture",
            },
        ])
        products.insert_many([  
            {
                '_id': ObjectId("10fefe4a1cad4140785928a4"),
                'name': "cutlery", 
                'description': "An interesting set of cutlery",
                'price': 5.99,
                'quantity':4,
                'categories': [ObjectId("22fefe4a1cad4140785928a4")],
            },
            {
                '_id': ObjectId("11fefe4a1cad4140785928a4"),
                'name': "chair",
                'description': "A comfortable armchair",
                'price': 29.99,
                'quantity':2,
                'categories': [
                    ObjectId("23fefe4a1cad4140785928a4"),
                    ObjectId("22fefe4a1cad4140785928a4"),
                ],
            },
            {
                '_id': ObjectId("12fefe4a1cad4140785928a4"),
                'name': "laptop",
                'description': "A powerful computing device",
                'price': 1299.99,
                'quantity':1,
                'categories': [ObjectId("21fefe4a1cad4140785928a4")],
            },
            {
                '_id': ObjectId("13fefe4a1cad4140785928a4"),
                'name': "headphones",  
                'description': "Wireless noise-cancelling headphones",
                'price': 99.99,
                'quantity':100,
                'categories': [ObjectId("21fefe4a1cad4140785928a4")],
            },
        ])
        return db  

    return db_creation
