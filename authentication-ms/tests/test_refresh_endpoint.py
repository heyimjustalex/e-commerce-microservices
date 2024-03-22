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
import datetime

envs: dict[str, str] = {
    'JWT_ACCESS_TOKEN_SECRET_KEY': 'accesstokenkey',
    'JWT_REFRESH_TOKEN_SECRET_KEY': "refreshtokenkey",
    'JWT_ACCESS_TOKEN_EXPIRE_MINUTES': '10080',
    'JWT_TOKEN_ALG': 'HS256',
    'JWT_REFRESH_TOKEN_EXPIRE_MINUTES': '30'
}

FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)

@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls, tz=None):
            return FAKE_TIME
    
    monkeypatch.setattr(datetime, 'datetime', mydatetime)
    return mydatetime
  

def test_GivenRefreshToken_When_Refresh_Then_ReturnAccessToken(
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch,
    patch_datetime_now

) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    monkeypatch.setattr(datetime,'datetime',patch_datetime_now)

     # Given
    user_data: dict[str, str] = {
        "email": "aaa@aaa.com",
        "password": "aaa@aaa.com",
        "role": "user"
    }


    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function
    app.dependency_overrides[datetime.datetime.now] = patch_datetime_now.now
    # When
    response: Response = client.post("/api/auth/login", json=user_data)
    response_json = response.json()
    print("LOGIN RESPONSE", response_json)
    # Mock DB

    # Given aaa@aaa.com refresh token
    user_data: dict[str, str] = {
        "refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFhYUBhYWEuY29tIiwicm9sZSI6InVzZXIiLCJleHAiOjE3MTExMzAyMDZ9.FNIg7Fo-EUpL0oZj2f4wfCJaBsOKrWxwHBd7oxY7J9M"
    }
    
    # When
    response: Response = client.post("/api/auth/refresh", json=user_data)
    response_json = response.json()
    print(response_json["access_token"])

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response_json
