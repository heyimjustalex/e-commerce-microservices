
from fastapi import Depends
from pymongo.database import Database
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.database.connector import Connector
from app.database.connector import Connector
from app.broker.consumers.consumer import MessageConsumer
from app.broker.producers.producer import MessageProducer
from pymongo import MongoClient

# def get_products_service(db: Database = Depends(Connector.get_db),client: MongoClient = Depends(Connector.get_db_client)) -> ProductService:
#     return ProductService(ProductRepository(db,client),CategoryRepository(db),MessageBroker())

def get_orders_service(db: Database = Depends(Connector.get_db,use_cache=True)) -> OrderService:
    return OrderService(OrderRepository(db))

# def get_message_consumer(db: Database = Depends(Connector.get_db,use_cache=True))->MessageConsumer:
#     return MessageConsumer(OrderRepository(db))

# def get_message_producer()->MessageProducer:
#     return MessageProducer()