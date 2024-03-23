from pydantic import BaseModel, Field,BeforeValidator
from typing import List,  Annotated
PyObjectId = Annotated[str, BeforeValidator(str)]

class Product(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    description: str
    price: float
    categories: List[PyObjectId]= Field(default=None)

class Category(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    name: str
    



