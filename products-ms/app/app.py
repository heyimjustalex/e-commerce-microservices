from fastapi import FastAPI
from app.exceptions.handlers import *
from app.exceptions.definitions import *
from app.controllers.products_controller import router as products_router
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
from app.brokers.consumers.consumer import MessageConsumer
from app.brokers.producers.producer import MessageProducer
from app.repositories.product_repository import ProductRepository
from app.database.connector import Connector

app = FastAPI()
app.add_exception_handler(ProductAlreadyExists,product_already_exists_exception_handler)
app.add_exception_handler(ProductIncorrectFormat,product_incorrect_format_exception_handler)
app.add_exception_handler(ProductNotFound, product_not_found_exception_handler)
app.add_exception_handler(CategoryNotFound, category_not_found_exception_handler)
app.add_exception_handler(BrokerMessagePublishError, broker_message_publish_exception_handler)

class ExtendedFastAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer :AIOKafkaConsumer 
        self.producer :AIOKafkaProducer

app = ExtendedFastAPI()

@app.on_event("startup")
async def startup():
    app.consumer = await MessageConsumer.startup_consumer()
    app.producer = await MessageProducer.startup_producer()
    product_repository = ProductRepository(Connector.get_db(), Connector.get_db_client())
    asyncio.create_task(MessageConsumer.consume(app.consumer,product_repository))    

@app.on_event("shutdown")
async def shutdown():
    await MessageConsumer.shutdown_consumer(app.consumer)
    
app.include_router(products_router)
 