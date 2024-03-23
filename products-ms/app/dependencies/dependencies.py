
from fastapi import Depends
from pymongo.database import Database
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.database.connector import Connector

def get_products_service(db: Database = Depends(Connector.get_db)) -> ProductService:
    return ProductService(ProductRepository(db))
