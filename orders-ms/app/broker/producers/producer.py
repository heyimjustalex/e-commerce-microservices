from aiokafka import  AIOKafkaProducer
import json


class MessageProducer:
    KAFKA_TOPIC:str = 'shop'
    KAFKA_GROUP:str = 'group'
    KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
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
        output: bytes = json.dumps(message).encode('utf-8')
        return output
