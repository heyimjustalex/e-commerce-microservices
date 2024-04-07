from pydantic import BaseModel, Field,BeforeValidator
from typing import List,  Annotated, Optional
PyObjectId = Annotated[str, BeforeValidator(str)]

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

class Product(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    description: str
    price: float
    quantity:int
    categories: List[PyObjectId]= Field(default=None)

class ProductCreateEvent(BaseModel):
    type: str
    product:Product

class OrderCreateEvent(BaseModel):

    type: str
    order: Order
    class Config:
        include_private_fields = True

class OrderStatusUpdateEvent(BaseModel):
    orderId:PyObjectId
    type: str
    status: str
    products: List[BoughtProduct]




