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

class Category(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str  

class ShopProductEvent(BaseModel):
    type: str
    product:Product
    class Config:
        include_private_fields = True


class ProductCreateEvent(BaseModel):
    type: str
    product:Product

class BoughtProduct(BaseModel):
    name: str
    price: Optional[float] = None
    quantity:int

class Order(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    client_email:str
    cost:float
    status: str
    products: List[BoughtProduct]

class OrderCreateEvent(BaseModel):
    type: str
    order:Order
  
class OrderStatusUpdateEvent(BaseModel):
    type: str
    status: str
    products: List[BoughtProduct]
