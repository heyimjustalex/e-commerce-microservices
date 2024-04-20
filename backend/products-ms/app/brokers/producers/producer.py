from aiokafka import AIOKafkaProducer
import json
import os
class MessageProducer:
    KAFKA_TOPIC:str = 'shop'
    KAFKA_GROUP:str = 'group'
    KAFKA_BOOTSTRAP_SERVERS:str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'message-broker:19092')
    isStarted = False
    _producer:AIOKafkaProducer

    @classmethod   
    async def get_producer(cls):  
        if not cls.isStarted:
            cls._producer: AIOKafkaProducer = await cls.startup_producer()
            cls.isStarted = True
        return cls._producer  
    
    @classmethod  
    async def startup_producer(cls):
        print("STARTUP PRODUCER")
        producer = AIOKafkaProducer(
            value_serializer=cls._serializer,        
            bootstrap_servers=cls.KAFKA_BOOTSTRAP_SERVERS,
        )      
        await producer.start() 
        return producer
    
    @classmethod      
    async def shutdown_producer(cls):
        if cls.isStarted:
            await cls._producer.stop()
            
    @classmethod  
    def _serializer(cls, message):
        test: bytes = json.dumps(message).encode('utf-8')
        return test
