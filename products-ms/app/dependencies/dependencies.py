
from fastapi import Depends
from pymongo.database import Database
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.database.connector import Connector

from pymongo import MongoClient
from app.brokers.producers.producer import MessageProducer

def get_products_service(db: Database = Depends(Connector.get_db),client: MongoClient = Depends(Connector.get_db_client)) -> ProductService:
    return ProductService(ProductRepository(db,client),CategoryRepository(db),MessageProducer())



