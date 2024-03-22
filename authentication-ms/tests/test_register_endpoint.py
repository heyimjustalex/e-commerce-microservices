from httpx import Response
from pymongo.collection import Collection
import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient as MockMongoClient
from fastapi import status
from pymongo.database import Database
from typing import Any, Callable
from app.database.connector import Connector
from tests.conftest.conftest import app, client
from tests.conftest.conftest import client, app, inmemory_database_creation_function

def test_Given_ProperUser_When_RegisteringTheUser_Then_CreatedRequestIsReturned(
    inmemory_database_creation_function: Callable[[], Database[Any]],
  
) -> None: 
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function
   
    # Given
    user_data: dict[str, str] = {
        "email": "test@test.com",
        "password": "password123",
            "role":"user"
    }
    # When
    response: Response = client.post("/api/auth/register", json=user_data)

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"email": "test@test.com", "role":"user"}

def test_Given_UserWithWrongEmailFromat_When_RegisteringTheUser_Then_BadRequestIsReturned(
    inmemory_database_creation_function: Callable[[], Database[Any]]
) -> None: 
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    # Given
    user_data: dict[str, str] = {
        "email": "test",
        "password": "password123",
        "role":"user"
    }
    # When
    response: Response = client.post("/api/auth/register", json=user_data)

    # Then    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'This e-mail is not acceptable'}

def test_Given_ExistingUser_When_RegisteringTheSameUser_Then_BadRequestIsReturned(
    inmemory_database_creation_function: Callable[[], Database[Any]]
) -> None: 
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function
    
    # Given
    user_data: dict[str, str] = {
        "email": "aaa@aaa.com",
        "password": "aaa@aaa.com",
        "role":"user"
    }
    
    # When
    response: Response = client.post("/api/auth/register", json=user_data)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()  == {'detail': 'This e-mail is not acceptable'}
