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

class ProductStub(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    price: Optional[float] = None
    quantity:int




class Category(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str  

class ShopProductEvent(BaseModel):
    type: str
    product:ProductStub
    class Config:
        include_private_fields = True

class ProductCreateEvent(BaseModel):
    type: str
    product:Product


class Order(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    client_email:str
    cost:float
    status: str
    products: List[ProductStub]

class OrderCreateEvent(BaseModel):
    type: str
    order:Order
   
class OrderStatusUpdateEvent(BaseModel):
    orderId:PyObjectId
    type: str
    status: str 

class ProductsQuantityUpdate(BaseModel):
    type: str
    products: List[ProductStub]

