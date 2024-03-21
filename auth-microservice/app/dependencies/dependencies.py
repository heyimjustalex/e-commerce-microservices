
from fastapi import Depends
from pymongo.database import Database
from services.user_service import UserService
from repositories.user_repository import UserRepository
from database.connector import Connector

def get_user_service(db: Database = Depends(Connector.get_db)) -> UserService:
    return UserService(UserRepository(db))
