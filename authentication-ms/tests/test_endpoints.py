from httpx import Response
from pymongo.collection import Collection
import pytest
from fastapi.testclient import TestClient
from fastapi import status
import sys  
from pymongo.database import Database
from typing import Any, Callable
import os
from mongomock import MongoClient as MockMongoClient
from app.database.connector import Connector
from app.app import app



client = TestClient(app)

@pytest.fixture()
def inmemory_database_creation_function() -> Callable[[], Database[Any]]:
    def db_creation() -> Database[Any]:
        client = MockMongoClient()  
        db: Database[Any] = client['shop']
        collection: Collection[Any] = db['users']
        collection.insert_one({'email': 'aaa@aaa.com', 'password_hash': '9c520caf74cff9b9a891be3694b20b3586ceb17f2891ceb1d098709c1e0969a3'})
        collection.insert_one({'email': 'bbb@bbb.com', 'password_hash': '77cd27bc3de668c18ed6be5f5c2909ffdacdf67705c30d132003ad5a89085deb'})
        return db 
    return db_creation

def test_register_endpoint_when_correct_credentials(
    inmemory_database_creation_function: Callable[[], Database[Any]]
) -> None: 
    
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    user_data: dict[str, str] = {
        "email": "test@test.com",
        "password": "password123"
    }
    response: Response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"email": "test@test.com"}

def test_register_endpoint_when_invalid_email_format(
    inmemory_database_creation_function: Callable[[], Database[Any]]
) -> None: 
    
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    user_data: dict[str, str] = {
        "email": "test",
        "password": "password123"
    }
    response: Response = client.post("/api/auth/register", json=user_data)

    print(response.json())
    print(type(response.json()))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'This e-mail is not acceptable'}

def test_register_endpoint_when_user_already_exists(
    inmemory_database_creation_function: Callable[[], Database[Any]]
) -> None: 
    
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    user_data: dict[str, str] = {
        "email": "aaa@aaa.com",
        "password": "aaa@aaa.com"
    }
    response: Response = client.post("/api/auth/register", json=user_data)
    print(response.json())
    print(type(response.json()))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()  == {'detail': 'This e-mail is not acceptable'}
