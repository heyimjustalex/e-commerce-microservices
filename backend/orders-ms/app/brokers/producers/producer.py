import os
import json
from aiokafka import  AIOKafkaProducer

class MessageProducer:
    KAFKA_TOPIC:str  = os.getenv('KAFKA_TOPIC', 'shop')
    KAFKA_GROUP:str =  os.getenv('KAFKA_GROUP', 'group')
    KAFKA_BOOTSTRAP_SERVERS:str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'message-broker:19092')
    isStarted = False
    _producer:AIOKafkaProducer

    @classmethod   
    async def get_producer(cls) -> AIOKafkaProducer:  
        if not cls.isStarted:
            cls._producer: AIOKafkaProducer = await cls.startup_producer()
            cls.isStarted = True
        return cls._producer  
    
    @classmethod  
    async def startup_producer(cls) -> AIOKafkaProducer:
        cls._producer = AIOKafkaProducer(
            value_serializer=cls._serializer,        
            bootstrap_servers=cls.KAFKA_BOOTSTRAP_SERVERS,
        )
        await cls._producer.start()
        return cls._producer
    
    @classmethod      
    async def shutdown_producer(cls) -> None:
        if cls.isStarted:
            await cls._producer.stop()
        cls.isStarted = False
            
    @classmethod  
    def _serializer(cls, message) -> bytes:
        return json.dumps(message).encode('utf-8')

