
from fastapi import Depends
from pymongo.database import Database
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.database.connector import Connector
from app.database.connector import Connector
from app.brokers.message_broker import MessageBroker
from pymongo import MongoClient

# def get_products_service(db: Database = Depends(Connector.get_db),client: MongoClient = Depends(Connector.get_db_client)) -> ProductService:
#     return ProductService(ProductRepository(db,client),CategoryRepository(db),MessageBroker())

def get_orders_service(db: Database = Depends(Connector.get_db)) -> OrderService:
    return OrderService(OrderRepository(db))
