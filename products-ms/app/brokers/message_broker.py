# from fastapi import FastAPI, HTTPException
# from confluent_kafka import Producer, Consumer, KafkaError
# import json
# import asyncio
# from app.models.models import ShopProductEvent
# from app.exceptions.definitions import BrokerMessagePublishError
# import jsonpickle

# import json
# from bson import ObjectId


# class MessageBroker:
#     KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
#     KAFKA_TOPIC:str = 'shop'
#     KAFKA_GROUP:str = 'group' 

#     def _kafka_producer(self):
#         conf: dict[str, str] = {
#         'bootstrap.servers': self.KAFKA_BOOTSTRAP_SERVERS,
#         'group.id': self.KAFKA_GROUP,
#         'auto.offset.reset': 'earliest', 
#         }
#         return Producer(**conf)

#     async def publish_message(self,event:ShopProductEvent):
#         producer = self._kafka_producer()
#         try:
#             print("BEFORE DUMP",event)
#             print("DUMP MODEL JSON", event.model_dump_json())
#             producer.produce(self.KAFKA_TOPIC, event.model_dump_json())
#             producer.flush()

#         except Exception as e:
#             print("EXCEPTION",e)
#             raise BrokerMessagePublishError()
