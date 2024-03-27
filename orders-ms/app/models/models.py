from pydantic import BaseModel, Field,BeforeValidator
from typing import List,  Annotated
PyObjectId = Annotated[str, BeforeValidator(str)]

class ProductItem(BaseModel):
    name: str
    price: float
    quantity:int


class Order(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    client_email:str
    cost:float
    status: str
    products: List[ProductItem]




