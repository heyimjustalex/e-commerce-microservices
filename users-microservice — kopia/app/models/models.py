from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class User(BaseModel):   
    _id: Optional[ObjectId] = None
    email:str
    password_hash:str

