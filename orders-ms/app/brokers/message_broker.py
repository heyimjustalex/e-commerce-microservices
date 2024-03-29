from fastapi import FastAPI, HTTPException
from confluent_kafka import Producer, Consumer, KafkaError
import json
import asyncio
from app.models.models import ShopProductEvent
from app.exceptions.definitions import BrokerMessagePublishError
import jsonpickle
class MessageBroker:
    KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
    KAFKA_TOPIC:str = 'shop'
    KAFKA_GROUP:str = 'group'
    def __init__(self) -> None:
        pass

    def _kafka_consumer(self):
        conf: dict[str, str] = {
        'bootstrap.servers': self.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': self.KAFKA_GROUP,
        'auto.offset.reset': 'earliest', 
        }
        return Consumer(**conf)

    def _kafka_producer(self):
        conf: dict[str, str] = {
        'bootstrap.servers': self.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': self.KAFKA_GROUP,
        'auto.offset.reset': 'earliest', 
        }
        return Producer(**conf)

    async def publish_message(self,event:ShopProductEvent):
        producer = self._kafka_producer()
        try:
            producer.produce(self.KAFKA_TOPIC, jsonpickle.encode(event))
            producer.flush()

        except Exception as e:
            print("EXCEPTION",e)
            raise BrokerMessagePublishError()

    async def subscribe_messages(self):
        consumer = self._kafka_consumer()
        consumer.subscribe([self.KAFKA_TOPIC])
        messages = []

        try:
            async def poll_messages():
                nonlocal messages
                while True:
                    message = await consumer.poll(timeout=1.0)
                    if message is None:
                        continue
                    if message.error():
                        print(f"Consumer error: {message.error()}")
                        continue
                    print(f"Received message: {message.value().decode('utf-8')}")
                    messages.append(json.loads(message.value().decode('utf-8')))

            # Start polling for messages asynchronously
            task = asyncio.create_task(poll_messages())

            # Wait for a certain period of time or until a condition is met
            await asyncio.sleep(10)  # Sleep for 10 seconds or any duration you want

            # Cancel the polling task
            task.cancel()

            print("All messages consumed.")
            return {"messages": messages}

        except asyncio.CancelledError:
            print("Polling task cancelled.")
            return {"messages": messages}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error occurred while subscribing to messages: {e}")

        finally:
            consumer.close()