from fastapi import APIRouter, Depends, status
from typing import List, Optional
import os

from app.services.category_service import CategoryService
from app.dependencies.dependencies import get_categories_service
from app.schemas.schemas import CategoryResponse, CategoriesResponse
from app.models.models import Category

router = APIRouter(
    prefix=os.getenv('API_PRODUCT_PREFIX','/api'),
    tags=['cat']
)

@router.get("/categories", response_model=CategoriesResponse, status_code=status.HTTP_200_OK)
def get_categories( service: CategoryService = Depends(get_categories_service)):
    categories : List[Category] = service.get_categories()
    response_categories : List[CategoryResponse] = [CategoryResponse(name=category.name) for category in categories]
    return CategoriesResponse(categories=response_categories)