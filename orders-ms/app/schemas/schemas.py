from pydantic import BaseModel
from app.models.models import BoughtProduct
from typing import List

class OrderCreateRequest(BaseModel):
    email:str
    products:List[BoughtProduct]

class OrdersRequest(BaseModel):
    email:str

class OrderCreatedResponse(BaseModel):
    status: str
    cost:float
    products: List[BoughtProduct]

class OrderResponse(BaseModel):
    status: str
    cost:float
    products: List[BoughtProduct]

class OrdersResponse(BaseModel):
    orders : List[OrderResponse]









