from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class User(BaseModel):   
    _id: Optional[ObjectId] = None
    email:str
    role:str
    password_hash:str

class Product(BaseModel):
    _id: Optional[ObjectId] = None
    name:str
    description:str
    price:float