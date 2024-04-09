from fastapi import FastAPI
import asyncio

from app.brokers.consumers.consumer import MessageConsumer
from app.repositories.product_repository import ProductRepository
from app.database.connector import Connector
from app.exceptions.handlers import *
from app.exceptions.definitions import *
from app.controllers.products_controller import router as products_router

app = FastAPI()   
app.include_router(products_router)
app.add_exception_handler(ProductAlreadyExists,product_already_exists_exception_handler)
app.add_exception_handler(ProductIncorrectFormat,product_incorrect_format_exception_handler)
app.add_exception_handler(ProductNotFound, product_not_found_exception_handler)
app.add_exception_handler(CategoryNotFound, category_not_found_exception_handler)
app.add_exception_handler(BrokerMessagePublishError, broker_message_publish_exception_handler)

@app.on_event("startup")
async def startup_event():    
    product_repository = ProductRepository(Connector.get_db(), Connector.get_db_client())
    asyncio.create_task(MessageConsumer.consume(product_repository))







