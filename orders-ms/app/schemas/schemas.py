from pydantic import BaseModel
from typing import List

from app.models.models import ProductStub,BoughtProductStub

class OrderCreateRequest(BaseModel):
    email:str
    products:List[BoughtProductStub]

class OrdersRequest(BaseModel):
    email:str

class OrderCreatedResponse(BaseModel):
    status: str
    cost:float
    products: List[ProductStub]

class OrderResponse(BaseModel):
    status: str
    cost:float
    products: List[ProductStub]

class OrdersResponse(BaseModel):
    orders : List[OrderResponse]









