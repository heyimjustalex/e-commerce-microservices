from pydantic import BaseModel, Field,BeforeValidator
from typing import List,  Annotated, Any, Dict
import json

PyObjectId = Annotated[str, BeforeValidator(str)]


class Category(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    

class Product(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    description: str
    price: float
    quantity:int
    categories: List[PyObjectId]= Field(default=None)


class ShopProductEvent(BaseModel):
    type: str
    product:Product


