from pydantic import BaseModel, validator, Field,BeforeValidator
from typing import Optional, List,  Annotated
from bson import ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        if not ObjectId.is_valid(v):
            raise ValueError(f'Invalid ObjectId: {v}')
        return str(v)


class Category(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    

class Product(BaseModel):
    _id: Optional[ObjectIdStr] = None
    name: str
    description: str
    price: float
    categories: List[ObjectIdStr] = Field(default=[])

    @validator("categories")
    def validate_categories(cls, v):
        for category_id in v:
            if not ObjectId.is_valid(category_id):
                raise ValueError(f'Invalid category ObjectId: {category_id}')
        return v
