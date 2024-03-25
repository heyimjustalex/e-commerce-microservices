from pydantic import BaseModel
from app.models.models import Product
from typing import List

class ProductRequestByName(BaseModel):
    name:str

class ProductCreateRequest(BaseModel):
    name:str
    description:str
    price:float   
    categories:List[str]

class ProductResponse(BaseModel):
    name:str
    description:str
    price:float
    categories:List[str]


class ProductsResponse(BaseModel):
    products:List[ProductResponse]





