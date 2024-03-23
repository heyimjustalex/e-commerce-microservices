
import re
from app.repositories.product_repository import ProductRepository
from hashlib import sha256
from app.schemas.schemas import ProductCreateRequest, ProductRequestByName
from app.exceptions.definitions import ProductNotFound, ProductAlreadyExists, ProductIncorrectFormat
from typing import Union, List
from models.models import Product

class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository: ProductRepository = repository

    def check_product_format(self, product:Product):
        if not re.match(r'^[a-zA-Z\s]+$', product.name):
            raise ProductIncorrectFormat(detail="Name should contain only letters and spaces")

        if not re.match(r'^[a-zA-Z\s]+$', product.description):
            raise ProductIncorrectFormat(detail="Description should contain only letters and spaces")

        if not isinstance(product.price, float):
            raise ProductIncorrectFormat(detail="Price should be a float")

        if product.price < 0:
            raise ProductIncorrectFormat(detail="Price should be a positive value")

        return True

    def get_products(self) -> List[Product]:
        return self.repository.get_products()
    
    def get_product_by_name(self, data:ProductRequestByName) -> Product:
        product : Union[Product, None] = self.repository.get_product_by_name(data.name)
        if not product:
           raise ProductNotFound()
        return product

    def create_product(self, data:ProductCreateRequest) -> Product:
        name :str = data.name
        description : str = data.description
        price : float = data.price 
        product : Product = Product(name=name, description=description, price=price)
        self.check_product_format(product)

        if self.repository.get_product_by_name(name):
            raise ProductAlreadyExists()
            
        return self.repository.create_product(product)

