from pydantic import BaseModel
from typing import List

class ProductRequestByName(BaseModel):
    name:str

class ProductItem(BaseModel):
    name: str
    description: str
    price: float
    quantity:int
    categories: List[str]

class ProductCreateRequest(BaseModel):
    product:ProductItem

class ProductResponse(BaseModel):
    name:str
    description:str
    price:float
    quantity:int
    categories:List[str]

class ProductsResponse(BaseModel):
    products:List[ProductResponse]





