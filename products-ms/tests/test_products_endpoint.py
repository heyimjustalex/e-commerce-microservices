from bson import ObjectId
from httpx import Response
from fastapi import status
from app import app
from pymongo.database import Database
from typing import Any, Callable
import os
from app.database.connector import Connector
from tests.conftest.conftest import MessageProducerMock,client_creation_function, client, app,envs, API_PRODUCT_PREFIX,inmemory_database_creation_function
from app.brokers.producers.producer import MessageProducer
import mongomock
import mock

# def test_GivenNonExistingProduct_When_Adding_Then_ProductIsAdded(
#     inmemory_database_creation_function: Callable[[], Database[Any]],
#     client_creation_function,
#     monkeypatch
# ) -> None: 
#     # Update ENV variables
#     monkeypatch.setattr(os, 'environ', envs)
#     # Mock DB
            
#     app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function
#     app.dependency_overrides[Connector.get_db_client] = client_creation_function
#     # app.dependency_overrides[MessageProducer.get_producer]=MessageProducerMock.get_producer
#     # Given
#     product_data:dict[str,Any] = {
#     "product":{
#     "name": "okhiiddi",
#     "quantity":"5",
#     "description": "An interestdddhing set of cutlery",
#     "price": 5.99,
#     "categories": ["kitchen" ]
#     }
#     }
    
#     # When
#     response: Response = client.post(API_PRODUCT_PREFIX+"/products", json=product_data)
#     response_json = response.json()
#     print(response_json)
#     # Then
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response_json['name']=='mixer'
#     assert response_json['description']=="An interesting set of cutlery"
#     assert response_json['price']==5.99
#     assert list(response_json['categories'])[0]=='kitchen'
#     assert "_id" not in response_json
#     assert "id" not in response_json


# def test_GivenProductWithoutCategories_When_Adding_Then_ProductAdded(
#     inmemory_database_creation_function: Callable[[], Database[Any]],
#     monkeypatch
# ) -> None: 
#     # Update ENV variables
#     monkeypatch.setattr(os, 'environ', envs)
#     # Mock DB
#     app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function


#     # Given
#     product_data:dict[str,Any] = {
#     "product":{
#     "name": "okhiiddi",
#     "quantity":"5",
#     "description": "An interestdddhing set of cutlery",
#     "price": 5.99,
#     "categories": ["kitchen" ]
#     }
#     }
    
#     # When
#     response: Response = client.post(API_PRODUCT_PREFIX+"/products", json=product_data)
#     response_json = response.json()
    
#     # Then
#     assert response.status_code == status.HTTP_201_CREATED
#     assert "_id" not in response_json
#     assert "id" not in response_json
#     assert response_json['name']=='mixer'
#     assert response_json['description']=="An interesting set of cutlery"
#     assert response_json['price']==5.99
#     assert list(response_json['categories'])==[]

# def test_GivenExistingProduct_When_Adding_Then_ResponseError(
#     inmemory_database_creation_function: Callable[[], Database[Any]],
#     monkeypatch
# ) -> None: 
#     # Update ENV variables
#     monkeypatch.setattr(os, 'environ', envs)
#     # Mock DB
#     app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

#     # Given
#     product_data:dict[str,Any] = {
#         'name': "headphones", 
#         'description': "Wireless noise-cancelling headphones",
#         'price': 99.99,
#         'categories': ["electornics"],
#     }
#     # When
#     response: Response = client.post(API_PRODUCT_PREFIX+"/products", json=product_data)
#     response_json = response.json()

#     # Then
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert response_json['detail'] == "Product already exists"
#     assert "_id" not in response_json
#     assert "id" not in response_json

def test_Given_Nothing_When_RequestingProducts_Then_ProductsAreReturned(
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function
    
    # Given

    # When
    response: Response = client.get(API_PRODUCT_PREFIX+"/products")
    response_json = response.json()
    returned_products:list=response_json['products']
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(returned_products)>0
    assert "_id" not in returned_products[0]
    assert "id" not in returned_products[0]

def test_Given_ProductName_When_RequestingExistingProductByName_Then_ProductIsReturned(
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function
    # Given

    # When
    response: Response = client.get(API_PRODUCT_PREFIX+"/products?name=laptop")
    response_json = response.json()
    returned_products:list=response_json['products']
    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(returned_products)>0
    assert "_id" not in returned_products[0]
    assert "id" not in returned_products[0]
    assert returned_products[0]['name']=='laptop'
    assert returned_products[0]['description']=="A powerful computing device"
    assert returned_products[0]['price']==1299.99
    assert len(list(returned_products[0]['categories']))>0

def test_Given_ProductName_When_RequestingNotExistingProductByName_Then_NotFoundIsReturned(
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    # Given

    # When
    response: Response = client.get(API_PRODUCT_PREFIX+"/products?name=notfoundprod")
    response_json = response.json()

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response_json
    

def test_Given_ProductCategoryName_When_RequestingNotExistingProductsByCategory_Then_ResponseNotFound(
    
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    # Given

    # When
    response: Response = client.get(API_PRODUCT_PREFIX+"/products/category?name=notfoundcategory")
    response_json = response.json()

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response_json
    
  
def test_Given_ProductCategoryName_When_RequestingExistingProductsByCategory_Then_ProductIsReturned(
    
    inmemory_database_creation_function: Callable[[], Database[Any]],
    monkeypatch
) -> None: 
    # Update ENV variables
    monkeypatch.setattr(os, 'environ', envs)
    # Mock DB
    app.dependency_overrides[Connector.get_db] = inmemory_database_creation_function

    # Given

    # When
    response: Response = client.get(API_PRODUCT_PREFIX+"/products?categoryName=kitchen")
    response_json = response.json()

    print("RESPONSE JSON", response_json)

    returned_products = response_json['products']

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(returned_products)>1
    assert "_id" not in returned_products[0]
    assert "id" not in returned_products[0]
    assert returned_products[0]['name']=='cutlery'
    assert returned_products[0]['description']=="An interesting set of cutlery"
    assert returned_products[0]['price']==5.99
    assert len(list(returned_products[0]['categories']))>0