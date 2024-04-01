
from fastapi import Depends
from pymongo.database import Database
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.database.connector import Connector
from app.database.connector import Connector
from app.broker.consumers.consumer import MessageConsumer
from app.broker.producers.producer import MessageProducer
from pymongo import MongoClient
from app.repositories.product_repository import ProductRepository

def get_orders_service(db: Database = Depends(Connector.get_db,use_cache=True),client:MongoClient = Depends(Connector.get_db_client, use_cache=True)) -> OrderService:
    return OrderService(OrderRepository(db,client), ProductRepository(db,client))

