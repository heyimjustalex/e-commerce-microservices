from fastapi import APIRouter, Depends, status
from app.schemas.schemas import ProductResponse, ProductsResponse, ProductCreateRequest
from app.services.product_service import ProductService
from typing import List, Optional
from app.models.models import Product
from app.dependencies.dependencies import get_products_service
import os
router = APIRouter(
    prefix=os.getenv('API_PRODUCT_PREFIX','/api/prod'),
    tags=['prod']
)


@router.get("/products", response_model=ProductsResponse, status_code=status.HTTP_200_OK)
def get_products(name: Optional[str] = None, service: ProductService = Depends(get_products_service)):
    if name:
        product:Product = service.get_product_by_name(name)
        products: List[Product] = [product]
        response:ProductsResponse = ProductsResponse(products=products)
    else:
        products: List[Product]= service.get_products()
        response : ProductsResponse = ProductsResponse(products=products)
    return response


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(data: ProductCreateRequest, service: ProductService = Depends(get_products_service)):
    product:Product=service.create_product(data)
    response:ProductResponse = ProductResponse(name=product.name, description=product.description, price= product.price, categories=product.categories)
    return response
@router.get("/products/category", response_model=ProductsResponse, status_code=status.HTTP_200_OK)
def get_products_by_categories(name: str, service:ProductService = Depends(get_products_service)):
    products:List[Product] = service.get_products_by_category(name)
    response:ProductsResponse = ProductsResponse(products=products)
    return response
