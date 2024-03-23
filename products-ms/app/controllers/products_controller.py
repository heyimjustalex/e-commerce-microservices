from fastapi import APIRouter, Depends, status
from app.schemas.schemas import ProductsRequest, ProductRequestByName, ProductResponse, ProductsResponse
from app.services.product_service import ProductService
from typing import List
from app.models.models import Product
from app.dependencies.dependencies import get_products_service
import os
router = APIRouter(
    prefix=os.getenv('API_PRODUCT_PREFIX','/api/prod'),
    tags=['prod']
)

@router.get("/products",response_model=ProductsResponse, status_code=status.HTTP_200_OK)
def get_products(data:ProductsRequest, service:ProductService = Depends(get_products_service)):
    products: List[Product]= service.get_products()
    response : ProductsResponse = ProductsResponse(products=products)
    return response

@router.get("/product/name/{product_name}", response_model=ProductResponse)
def get_product_by_name(data:ProductRequestByName, service:ProductService = Depends(get_products_service)):
    product:Product = service.get_product_by_name(data)
    response:ProductResponse = ProductResponse(name=product.name, description=product.description, price=product.price)
    return response
