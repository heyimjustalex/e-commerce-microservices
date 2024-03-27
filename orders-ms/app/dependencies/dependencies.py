
from fastapi import Depends
from pymongo.database import Database
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository
from app.database.connector import Connector

def get_orders_service(db: Database = Depends(Connector.get_db)) -> OrderService:
    return OrderService(OrderRepository(db))
