
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
API_PRODUCT_PREFIX:str = os.getenv('API_PRODUCT_PREFIX','/api')

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
        orders : Collection[Any] = db['orders']

        orders.insert_many([
        {
            '_id': ObjectId("71fefe4a1cad4140785928a4"),
            'client_email': "aaa@aaa.com",
            'status': "PENDING",
            'cost': 83.94,
            'products': [
            {
                'name': "cutlery",
                'price': 5.99,
                'quantity': 4,
            },
            {
                'name': "chair",
                'price': 29.99,
                'quantity': 2,
            },
            ],
        },
        {
            '_id': ObjectId("72fefe4a1cad4140785928a4"),
            'client_email': "bbb@bbb.com",
            'status': "ACCEPTED",
            'cost': 1299.99,
            'products': [
            {
                'name': "laptop",
                'price': 1299.99,
                'quantity': 1,
            },
            ],
        },
        {
            '_id': ObjectId("73fefe4a1cad4140785928a4"),
            'client_email': "ccc@ccc.com",
            'status': "PENDING",
           'cost': 699.93,
            'products': [
            {
                'name': "headphones",
                'price': 99.99,
                'quantity': 7,
            },
            ],
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
