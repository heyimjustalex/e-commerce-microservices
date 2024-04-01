from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
from json.decoder import JSONDecodeError
from app.models.models import *
from app.models.models import ShopProductEvent
from pydantic import BaseModel

class MessageProducer:
    KAFKA_TOPIC:str = 'shop'
    KAFKA_GROUP:str = 'group'
    KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
    isStarted = False
    _producer:AIOKafkaProducer

    @classmethod   
    async def get_producer(cls):  
        if not cls.isStarted:
            cls._producer: AIOKafkaProducer = await cls._create_producer()
            cls.isStarted = True
            print("CREATING")
        return cls._producer  
    
    @classmethod  
    async def _create_producer(cls):
        producer = AIOKafkaProducer(
            value_serializer=cls._serializer,        
            bootstrap_servers=cls.KAFKA_BOOTSTRAP_SERVERS,
        )
        print("STARTINGS")
        await producer.start()
        print("STARTEDS")
        return producer
    
    @classmethod      
    async def shutdown_producer(cls):
        if cls.isStarted:
            await cls._producer.stop()
            
    @classmethod  
    def _serializer(cls, message):
        test: bytes = json.dumps(message).encode('utf-8')
        return test
