from fastapi import APIRouter, Depends, status
from typing import List
import asyncio
import sys

from app.schemas.schemas import OrderResponse, OrderCreateRequest, OrderCreatedResponse,OrdersResponse
from app.services.order_service import OrderService
from app.dependencies.dependencies import get_orders_service
from app.models.models import Order

import os
router = APIRouter(
    prefix=os.getenv('API_PRODUCT_PREFIX','/api'),
    tags=['ord']
)

@router.post("/orders", response_model=OrderCreatedResponse, status_code=status.HTTP_201_CREATED)
async def add_order(data: OrderCreateRequest, service: OrderService = Depends(get_orders_service)):
    order:Order= await service.create_order_with_event_OrderCreate(data=data)
    response:OrderCreatedResponse = OrderCreatedResponse(cost=order.cost,status=order.status, products=order.products)
    return response

@router.get("/orders", response_model=OrdersResponse, status_code=status.HTTP_200_OK)
def get_orders(email:str, service: OrderService = Depends(get_orders_service)):
    orders:List[Order] = service.get_orders_by_email(email)
    orders_response: List[OrderResponse] = [OrderResponse(status=order.status, cost=order.cost, products=order.products) for order in orders]  
    response:OrdersResponse = OrdersResponse(orders=orders_response)
    return response

@router.get("/orders_error")
async def error():
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.stop()
    sys.exit(0)