from pydantic import BaseModel, Field,BeforeValidator
from typing import List,  Annotated, Optional
PyObjectId = Annotated[str, BeforeValidator(str)]

class BuyProductItem(BaseModel):
    name: str
    price: Optional[float] = None
    quantity:int

class Order(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    client_email:str
    cost:float
    status: str
    products: List[BuyProductItem]

class Product(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    description: str
    price: float
    quantity:int
    categories: List[PyObjectId]= Field(default=None)


class ShopProductEvent(BaseModel):
    type: str
    product:Product





