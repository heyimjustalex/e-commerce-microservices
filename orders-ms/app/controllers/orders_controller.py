from fastapi import APIRouter, Depends, status
from app.schemas.schemas import OrderResponse, OrderCreateRequest,OrdersRequest, OrderCreatedResponse,OrdersResponse
from app.services.order_service import OrderService
from typing import List, Optional
from app.models.models import  Order
from app.dependencies.dependencies import get_orders_service
import os
router = APIRouter(
    prefix=os.getenv('API_PRODUCT_PREFIX','/api'),
    tags=['prod']
)

@router.post("/orders", response_model=OrderCreatedResponse, status_code=status.HTTP_201_CREATED)
def add_order(data: OrderCreateRequest, service: OrderService = Depends(get_orders_service)):
    order:Order=service.create_order(data)
    response:OrderCreatedResponse = OrderCreatedResponse(cost=order.cost,status=order.status, products=order.products)
    return response

@router.get("/orders", response_model=OrdersResponse, status_code=status.HTTP_200_OK)
def get_orders(data: OrdersRequest, service: OrderService = Depends(get_orders_service)):
    orders:List[Order] = service.get_orders_by_email(data)
    orders_response: List[OrderResponse] = [OrderResponse(status=order.status, cost=order.cost, products=order.products) for order in orders]  
    response:OrdersResponse = OrdersResponse(orders=orders_response)
    return response
