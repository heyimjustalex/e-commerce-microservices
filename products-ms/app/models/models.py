from pydantic import BaseModel, Field,BeforeValidator
from typing import List,  Annotated

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


