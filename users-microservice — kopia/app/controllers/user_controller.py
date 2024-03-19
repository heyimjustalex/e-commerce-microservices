from fastapi import APIRouter, Depends
from pymongo.database import Database
from app.schemas.schemas import UserCreate, RegisterResponse
from app.services.user_service import UserService
from app.database.connector import Connector

router = APIRouter()

@router.post("/register",response_model=RegisterResponse)
def register(user_data: UserCreate, db: Database = Depends(Connector.get_db)):
    user_service = UserService(db)
    user_service.create_user(user_data.email, user_data.password)
    return RegisterResponse(message="Registration successful. Welcome!")

@router.post("/login")
def login():
    return {"login"}
