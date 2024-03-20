from fastapi import APIRouter, Depends, status, Response
from pymongo.database import Database
from app.schemas.schemas import UserCreate, UserRegisterResponse
from app.services.user_service import UserService
from app.database.connector import Connector
from app.models.models import User
from app.dependencies.dependencies import get_user_service
import jwt
router = APIRouter(
    prefix='/api/auth',
    tags=['auth']
)

@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, service:UserService = Depends(get_user_service)):   
    user:User = service.create_user(data.email, data.password)
    return UserRegisterResponse(email=user.email)

@router.post("/login",)
def login(form_data, service:UserService = Depends(get_user_service)):
    return {"login"}
