
from fastapi import Depends
from pymongo.database import Database
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.database.connector import Connector

def get_products_service(db: Database = Depends(Connector.get_db)) -> ProductService:
    return ProductService(ProductRepository(db),CategoryRepository(db))
