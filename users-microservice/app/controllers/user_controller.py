from fastapi import APIRouter, Depends
from pymongo.database import Database
from app.schemas.schemas import UserCreate, RegisterResponse
from app.services.user_service import UserService
from app.database.connector import Connector
from app.dependencies.dependencies import get_user_service
router = APIRouter()

@router.post("/register",response_model=RegisterResponse)
def register(user_data: UserCreate,service:UserService = Depends(get_user_service)):   
    service.create_user(user_data.email, user_data.password)
    return RegisterResponse(message="Registration successful. Welcome!")

@router.post("/login")
def login():
    return {"login"}
