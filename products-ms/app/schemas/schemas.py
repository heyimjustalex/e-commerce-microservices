from pydantic import BaseModel
from app.models.models import Product
from typing import List

class ProductRequestByName(BaseModel):
    name:str

class ProductCreateRequest(BaseModel):
    name:str
    description:str
    price:float   

class ProductsRequest(BaseModel):
    pass

class ProductResponse(BaseModel):
    name:str
    description:str
    price:float

class ProductsResponse(BaseModel):
    products:List[Product]



class UserRegisterRequest(BaseModel):
    email:str
    password:str

class UserLoginRequest(BaseModel):
    email:str
    password:str

class RefreshTokenRequest(BaseModel):
    refresh_token:str
    
class UserRegisterResponse(BaseModel):
    email: str
    role: str

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    access_token:str
   


