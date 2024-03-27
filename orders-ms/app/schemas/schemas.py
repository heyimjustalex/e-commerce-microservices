from pydantic import BaseModel
from app.models.models import ProductItem
from typing import List

class OrderCreateRequest(BaseModel):
    access_token:str
    products:List[ProductItem]

class OrdersRequest(BaseModel):
    access_token:str

class OrderCreatedResponse(BaseModel):
    status: str
    cost:float
    products: List[ProductItem]

class OrderResponse(BaseModel):
    status: str
    cost:float
    products: List[ProductItem]

class OrdersResponse(BaseModel):
    orders : List[OrderResponse]









