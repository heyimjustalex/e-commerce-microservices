
from fastapi import Depends
from pymongo.database import Database
from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.repositories.user_repository import UserRepository
from app.database.connector import Connector

def get_user_service(db: Database = Depends(Connector.get_db)) -> UserService:
    return UserService(UserRepository(db))
def get_token_service(db: Database = Depends(Connector.get_db)) -> TokenService:
    return TokenService(UserRepository(db))
