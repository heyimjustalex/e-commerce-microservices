from pydantic import BaseModel
from app.models.models import ProductStub,BoughtProductStub
from typing import List

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









