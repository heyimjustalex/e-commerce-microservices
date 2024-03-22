from httpx import Response
from pymongo.collection import Collection
import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient as MockMongoClient
from fastapi import status
from app import app
from pymongo.database import Database
from typing import Any, Callable
import os
from app.database.connector import Connector
from tests.conftest.conftest import client, app, inmemory_database_creation_function


envs: dict[str, str] = {
    'JWT_ACCESS_TOKEN_SECRET_KEY': 'accesstokenkey',
    'JWT_REFRESH_TOKEN_SECRET_KEY': "refreshtokenkey",
    'JWT_ACCESS_TOKEN_EXPIRE_MINUTES': '10080',
    'JWT_TOKEN_ALG': 'HS256',
    'JWT_REFRESH_TOKEN_EXPIRE_MINUTES': '30'
}


def test_GivenNonExistingAccount_When_LogingIn_Then_UnauthorizedtIsReturned(
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    # Given
    user_data: dict[str, str] = {
        "email": "idontexist@d9fc5f.com",
        "password": "47c8957f0bc6760603a8",
        "role": "user"
    }
    
    # When
    response: Response = client.post("/api/auth/login", json=user_data)
    response_json = response.json()

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "access_token" not in response_json
    assert "refresh_token" not in response_json


def test_GivenBadEmailFormat_When_LogingIn_Then_UnauthorizedtIsReturned(
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    # Given
    user_data: dict[str, str] = {
        "email": "bademailformat",
        "password": "47c8957f0bc6760603a8",
        "role": "user"
    }
    
    # When
    response: Response = client.post("/api/auth/login", json=user_data)
    response_json = response.json()
  
    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "access_token" not in response_json
    assert "refresh_token" not in response_json

def test_GivenExistingAccount_When_LogingIn_Then_ResponseParametersAreOk(
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    # Given
    user_data: dict[str, str] = {
        "email": "a64cb39621534d604e02@d9fc5f.com",
        "password": "4765a267d375eb7010dd0b3a051c96a16762d818f88e27c8957f0bc6760603a8",
        "role": "user"
    }
    
    # When
    response: Response = client.post("/api/auth/login", json=user_data)
    response_json = response.json()

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response_json
    assert "refresh_token" in response_json
    assert response_json["access_token"] != ""
    assert response_json["refresh_token"] != ""
    assert response.headers["Token-Type"] == "Bearer"