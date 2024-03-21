from typing import Union, Any
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.repositories.user_repository import UserRepository
from datetime import datetime, timedelta, timezone
from app.models.models import User
from app.schemas.schemas import UserLoginRequest
import jwt

JWT_SECRET_KEY : Union[str, None]  = os.getenv('JWT_SECRET_KEY')

JWT_ACCESS_TOKEN_EXPIRE_MINUTES : int = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES',7*24*60))
JWT_ACCESS_TOKEN_ALG : Union[str, None] = os.getenv('JWT_ACCESS_TOKEN_ALG')
JWT_REFRESH_TOKEN_EXPIRE_MINUTES : int = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES',30))

class TokenService:
    def __init__(self) -> None:
        pass 
    
    def create_access_token(self, data:User) -> str:
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        data_to_encode:dict[str,Any] = {"email":data.email,"role":data.role, "exp":expire}
        encoded_jwt:str = jwt.encode(data_to_encode,str(JWT_SECRET_KEY),str(JWT_ACCESS_TOKEN_ALG))
        return encoded_jwt
    
    def create_refresh_token(self, data:User) -> str:
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
        data_to_encode:dict[str,Any] = {"email":data.email,"role":data.role, "exp":expire}
        encoded_jwt:str = jwt.encode(data_to_encode,str(JWT_SECRET_KEY),str(JWT_ACCESS_TOKEN_ALG))
        return encoded_jwt