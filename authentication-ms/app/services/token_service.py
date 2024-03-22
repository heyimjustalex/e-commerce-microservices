from typing import Union, Any
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.repositories.user_repository import UserRepository
from datetime import datetime, timedelta, timezone
from app.models.models import User
from app.schemas.schemas import UserLoginRequest, RefreshTokenRequest
import jwt

from jwt.exceptions import InvalidTokenError
from app.exceptions.definitions import RefreshTokenInvalid


class TokenService:
    def __init__(self, user_repository:UserRepository) -> None:
        self.user_repository: UserRepository = user_repository
        
        self.JWT_ACCESS_TOKEN_SECRET_KEY : Union[str, None]  = os.getenv('JWT_ACCESS_TOKEN_SECRET_KEY')
        self.JWT_REFRESH_TOKEN_SECRET_KEY : Union[str, None]  = os.getenv('JWT_REFRESH_TOKEN_SECRET_KEY')
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES : int = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES',7*24*60))
        self.JWT_TOKEN_ALG : Union[str, None] = os.getenv('JWT_TOKEN_ALG')
        self.JWT_REFRESH_TOKEN_EXPIRE_MINUTES : int = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES',30))

    def create_access_token(self, data:User) -> str:
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        print("ACCECSS TOKEN CREATE", expire)
        data_to_encode:dict[str,Any] = {"email":data.email,"role":data.role, "exp":expire}
        encoded_jwt:str = jwt.encode(data_to_encode,str(self.JWT_ACCESS_TOKEN_SECRET_KEY),str(self.JWT_TOKEN_ALG))
        return encoded_jwt
    
    def create_refresh_token(self, data:User) -> str:
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=self.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
        data_to_encode:dict[str,Any] = {"email":data.email,"role":data.role, "exp":expire}
        encoded_jwt:str = jwt.encode(data_to_encode,str(self.JWT_REFRESH_TOKEN_SECRET_KEY),str(self.JWT_TOKEN_ALG))
        return encoded_jwt
    
    def refresh_access_token(self, data:RefreshTokenRequest): 
        try:
            decoded_jwt:dict[str,Any]= jwt.decode(data.refresh_token,str(self.JWT_REFRESH_TOKEN_SECRET_KEY),[str(self.JWT_TOKEN_ALG)])
            email:str = decoded_jwt['email']
            exp:float = decoded_jwt['exp']
            if not email or not exp:
                raise RefreshTokenInvalid()
            
            user:Union[User, None] = self.user_repository.get_user_by_email(email)
            if not user:
                raise RefreshTokenInvalid()
    
            expiration_time: datetime = datetime.fromtimestamp(exp).replace(tzinfo=timezone.utc)
            if expiration_time < datetime.now(timezone.utc):
                raise RefreshTokenInvalid()

            new_access_token: str = self.create_access_token(user)

        except InvalidTokenError:
            raise RefreshTokenInvalid()
        
        return new_access_token
