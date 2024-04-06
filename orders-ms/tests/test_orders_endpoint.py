from httpx import Response
from fastapi import status
from app import app
from pymongo.database import Database
from typing import Any, Callable
import os
from app.database.connector import Connector
from tests.conftest.conftest import client, app,envs, API_PRODUCT_PREFIX,inmemory_database_creation_function


def test_Nothing_When_GettingOrders_Then_Get(
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    # Given
 
    # When
    response: Response = client.get(API_PRODUCT_PREFIX+"/orders?email=aaa@aaa.com")
    response_json = response.json()
    response_json_orders = response_json['orders']

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response_json_orders[0]['status']=='PENDING'
    assert response_json_orders[0]['cost']==83.94
    assert response_json_orders[0]['products'][0]['name']=='cutlery'
    assert response_json_orders[0]['products'][0]['price']==5.99
    assert response_json_orders[0]['products'][0]['quantity']==4    
    assert "_id" not in response_json
    assert "id" not in response_json
    assert "_id" not in response_json_orders[0]['products'][0]
    assert "id" not in response_json_orders[0]['products'][0]
