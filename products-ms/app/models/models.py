from pydantic import BaseModel, Field,BeforeValidator
from typing import List,  Annotated, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]

class Product(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    description: str
    price: float
    quantity:int
    categories: List[PyObjectId]= Field(default=None)
    class Config:
        include_private_fields = True

# Product for generating events for order-ms (it doesn't need more)
class ProductStub(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    price: Optional[float] = None
    quantity:int

class Category(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str  

class Order(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    client_email:str
    cost:float
    status: str
    products: List[ProductStub]

# Event models

class ProductCreateEvent(BaseModel):
    type: str
    product:ProductStub
    class Config:
        include_private_fields = True

class OrderCreateEvent(BaseModel):
    type: str
    order:Order
   
class OrderStatusUpdateEvent(BaseModel):
    order_id:PyObjectId
    type: str
    status: str

class ProductsQuantityUpdate(BaseModel):
    type: str
    products: List[ProductStub]

