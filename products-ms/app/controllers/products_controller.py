from fastapi import APIRouter, Depends, status
from app.schemas.schemas import ProductsRequest, ProductRequestByName, ProductResponse, ProductsResponse
from app.services.product_service import ProductService
from typing import List, Tuple
from app.models.models import Product
from app.dependencies.dependencies import get_products_service
import os
router = APIRouter(
    prefix=os.getenv('API_PRODUCT_PREFIX','/api/prod'),
    tags=['prod']
)

@router.get("/products",response_model=ProductsResponse, status_code=status.HTTP_200_OK)
def get_products(service:ProductService = Depends(get_products_service)):
    products: List[Product]= service.get_products()
    response : ProductsResponse = ProductsResponse(products=products)
    return response

@router.get("/products/{product_name}", response_model=ProductResponse)
def get_product_by_name(product_name: str, service:ProductService = Depends(get_products_service)):
    product:Tuple[Product, List] = service.get_product_by_name(product_name)
    response:ProductResponse = ProductResponse(name=product[0].name, description=product[0].description, price=product[0].price, categories=product[1])
    return response

# @router.get("/products/category/{category_name}", response_model=ProductResponse)
# def get_products_by_categories(product_name: str, service:ProductService = Depends(get_products_service)):
#     product:Product = service.get_product_by_name(product_name)
#     response:ProductResponse = ProductResponse(name=product.name, description=product.description, price=product.price)
#     return response
