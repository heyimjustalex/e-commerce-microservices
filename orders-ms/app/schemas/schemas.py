from pydantic import BaseModel
from app.models.models import BuyProductItem
from typing import List

class OrderCreateRequest(BaseModel):
    access_token:str
    products:List[BuyProductItem]

class OrdersRequest(BaseModel):
    access_token:str

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









