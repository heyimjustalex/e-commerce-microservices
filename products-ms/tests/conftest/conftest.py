
from pymongo.database import Database
from typing import Any, Callable
from pymongo.collection import Collection
import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient as MockMongoClient
import os
from bson.objectid import ObjectId
from app.app import app
client = TestClient(app)
API_PRODUCT_PREFIX:str = os.getenv('API_PRODUCT_PREFIX','/api/prod')

envs: dict[str, str] = {
    'JWT_ACCESS_TOKEN_SECRET_KEY': 'accesstokenkey',
    'JWT_REFRESH_TOKEN_SECRET_KEY': "refreshtokenkey",
    'JWT_ACCESS_TOKEN_EXPIRE_MINUTES': '10080',
    'JWT_TOKEN_ALG': 'HS256',
    'JWT_REFRESH_TOKEN_EXPIRE_MINUTES': '30'
}


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
                'categories': [ObjectId("22fefe4a1cad4140785928a4")],
            },
            {
                '_id': ObjectId("11fefe4a1cad4140785928a4"),
                'name': "chair",
                'description': "A comfortable armchair",
                'price': 29.99,
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
                'categories': [ObjectId("21fefe4a1cad4140785928a4")],
            },
            {
                '_id': ObjectId("13fefe4a1cad4140785928a4"),
                'name': "headphones",  
                'description': "Wireless noise-cancelling headphones",
                'price': 99.99,
                'categories': [ObjectId("21fefe4a1cad4140785928a4")],
            },
        ])
        return db  

    return db_creation
