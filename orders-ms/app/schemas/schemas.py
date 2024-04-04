from pydantic import BaseModel
from app.models.models import BuyProductItem
from typing import List

class OrderCreateRequest(BaseModel):
    email:str
    products:List[BuyProductItem]

class OrdersRequest(BaseModel):
    email:str

class OrderCreatedResponse(BaseModel):
    status: str
    cost:float
    products: List[BuyProductItem]

class OrderResponse(BaseModel):
    status: str
    cost:float
    products: List[BuyProductItem]

class OrdersResponse(BaseModel):
    orders : List[OrderResponse]









