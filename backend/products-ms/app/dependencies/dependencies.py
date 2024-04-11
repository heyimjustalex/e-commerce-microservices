
from fastapi import Depends
from pymongo.database import Database
from pymongo import MongoClient

from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.database.connector import Connector
from app.services.category_service import CategoryService

def get_products_service(db: Database = Depends(Connector.get_db),client: MongoClient = Depends(Connector.get_db_client)) -> ProductService:
    return ProductService(ProductRepository(db,client),CategoryRepository(db))

def get_categories_service(db: Database = Depends(Connector.get_db),client: MongoClient = Depends(Connector.get_db_client)) -> CategoryService:
    return CategoryService(CategoryRepository(db))





