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
from tests.conftest.conftest import client, inmemory_database_creation_function,app
from datetime import datetime
from freezegun import freeze_time
envs: dict[str, str] = {
    'JWT_ACCESS_TOKEN_SECRET_KEY': 'accesstokenkey',
    'JWT_REFRESH_TOKEN_SECRET_KEY': "refreshtokenkey",
    'JWT_ACCESS_TOKEN_EXPIRE_MINUTES': '10080',
    'JWT_TOKEN_ALG': 'HS256',
    'JWT_REFRESH_TOKEN_EXPIRE_MINUTES': '30'
}


def test_GivenRefreshToken_When_Refresh_Then_ReturnAccessToken(
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch,
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function
          
    # Given aaa@aaa.com refresh token
    user_data: dict[str, str] = {
        "refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFhYUBhYWEuY29tIiwicm9sZSI6InVzZXIiLCJleHAiOjEzMjY1MDEwMDB9.oVVF9ruy37bocuJar-W0xALIOWgVfvPRdFXL9rCCN78"
    }
    with freeze_time("2012-01-14"):
    # When
        response: Response = client.post("/api/auth/refresh", json=user_data)
        response_json = response.json()

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response_json
    assert response_json["access_token"]=="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFhYUBhYWEuY29tIiwicm9sZSI6InVzZXIiLCJleHAiOjEzMjcxMDQwMDB9.bHk3QXaRko6KJfIGUM4wln11UOTCYmXZ1pDR2Tcszds"
