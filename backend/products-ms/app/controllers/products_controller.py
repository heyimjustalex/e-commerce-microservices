from fastapi import APIRouter, Depends, status
from typing import List, Optional
import os
import sys
from app.models.models import Product
from app.services.product_service import ProductService
from app.dependencies.dependencies import get_products_service
from app.schemas.schemas import ProductResponse, ProductsResponse, ProductCreateRequest
import asyncio

router = APIRouter(
    prefix=os.getenv('API_PRODUCT_PREFIX','/api'),
    tags=['prod']
)

@router.get("/products", response_model=ProductsResponse, status_code=status.HTTP_200_OK)
def get_products(name: Optional[str] = None, categoryName:Optional[str]=None, service: ProductService = Depends(get_products_service)):
    if name:
        product:Product = service.get_product_by_name(name)
        product_response:ProductResponse = ProductResponse(name=product.name, description=product.description,price=product.price, categories=product.categories, quantity=product.quantity)
        products_response: List[ProductResponse] = [product_response]
        response:ProductsResponse = ProductsResponse(products=products_response)
    elif categoryName:
        products_by_category:List[Product] = service.get_products_by_category(categoryName)
        products_response: List[ProductResponse] = [ProductResponse(name=product.name, description=product.description, price=product.price, categories=product.categories,quantity=product.quantity) for product in products_by_category]
        response : ProductsResponse = ProductsResponse(products= products_response) 
    else:
        products: List[Product]= service.get_products()
        print("PRODUCTS2", products)
        products_response: List[ProductResponse] = [ProductResponse(name=product.name, description=product.description, price=product.price, categories=product.categories,quantity=product.quantity) for product in products] 
        response : ProductsResponse = ProductsResponse(products= products_response)
    return response

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def add_product(data: ProductCreateRequest ,product_service: ProductService = Depends(get_products_service)):
    product:Product= await product_service.create_product_with_event_ProductCreate(data)
    response:ProductResponse = ProductResponse(name=product.name, description=product.description, price= product.price, categories=product.categories,quantity=product.quantity)
    return response


@router.get("/products_error")
async def error():
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.stop()
    sys.exit(0)