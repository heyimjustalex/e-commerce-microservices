from pydantic import BaseModel, Field,BeforeValidator
from typing import List,  Annotated, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]

class ProductStub(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    price: float
    quantity:int

class BoughtProductStub(BaseModel):
    name: str
    quantity:int

class Order(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    client_email:str
    cost:float
    status: str
    products: List[ProductStub]

class Product(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    description: str
    price: float
    quantity:int
    categories: List[PyObjectId]= Field(default=None)

# Event models, related to broker consumer/producer

class ProductCreateEvent(BaseModel):
    type: str
    product:ProductStub

class OrderCreateEvent(BaseModel):
    type: str
    order: Order
    class Config:
        include_private_fields = True

class OrderStatusUpdateEvent(BaseModel):
    order_id:PyObjectId
    type: str
    status: str


class ProductsQuantityUpdate(BaseModel):
    type: str
    products: List[ProductStub]





