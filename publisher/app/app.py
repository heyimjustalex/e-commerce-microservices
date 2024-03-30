from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
from app.models.models import *
from app.broker.broker import MessageBroker
            
class ExtendedFastAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer :AIOKafkaConsumer 
        self.producer :AIOKafkaProducer

app = ExtendedFastAPI()


@app.on_event("startup")
async def startup():
    app.consumer = await MessageBroker.startup_consumer()
    asyncio.create_task(MessageBroker.consume(app.consumer))    

@app.on_event("shutdown")
async def shutdown():
    await MessageBroker.shutdown_consumer(app.consumer)

