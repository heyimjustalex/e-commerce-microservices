from pydantic import BaseModel, validator, Field
from typing import Optional, List
from bson import ObjectId

class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        if not ObjectId.is_valid(v):
            raise ValueError(f'Invalid ObjectId: {v}')
        return str(v)

class User(BaseModel):   
    _id: Optional[ObjectIdStr] = None
    email: str
    role: str
    password_hash: str

class Category(BaseModel):
    _id: Optional[ObjectIdStr] = None
    name: str

class Product(BaseModel):
    _id: Optional[ObjectIdStr] = None
    name: str
    description: str
    price: float
    categories: List[ObjectIdStr] = Field(default=[])

    @validator("categories")
    def validate_categories(cls, v):
        for category_id in v:
            if not ObjectId.is_valid(category_id):
                raise ValueError(f'Invalid category ObjectId: {category_id}')
        return v
