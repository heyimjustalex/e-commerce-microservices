from fastapi import FastAPI, HTTPException
from confluent_kafka import Producer, Consumer, KafkaError
import json
import logging
import time
from app.models import *
app = FastAPI()
from fastapi.responses import JSONResponse
import jsonpickle
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
KAFKA_TOPIC:str = 'shop'
KAFKA_GROUP:str = 'group'

def kafka_consumer():
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'earliest',
  #      'fetch.min.bytes': 1,  # Fetch messages as soon as there is one byte available
       # 'fetch.max.wait.ms': 0  # Do not wait for more messages to accumulate, fetch immediately
    }
    return Consumer(**conf)

def kafka_producer():
    conf = {        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'earliest'}
    return Producer(**conf)


@app.post("/publish/")
async def publish_message(message: dict):
    # Initialize Kafka producer
    producer = kafka_producer()

    try:
        # Produce message to Kafka topic
        producer.produce(KAFKA_TOPIC, jsonpickle.decode(message))
        # Flush producer to ensure message is sent
        producer.flush()
        return {"message": "Message published successfully"}
    except KafkaError as e:
        raise HTTPException(status_code=500, detail=f"Error publishing message to Kafka: {e}")



@app.get("/subscribe/",response_model=ShopProductEvent)
async def subscribe_messages():
    # Initialize Kafka consumer
    consumer = kafka_consumer()

    # Subscribe to Kafka topic
    consumer.subscribe([KAFKA_TOPIC])

    messages = []

    try:
        i = 0
        while i < 5:
            i += 1
            print("Iteration:", i)
            message = consumer.poll(10.0)  # Poll for 1 second

            if message is None:
                print("No message received.")
                continue

            if message.error():
                print(f"Consumer error: {message.error()}")
                continue
            


            try:
                # Create a ShopProductEvent instance
                print(f"Received message: {message.value().decode('utf-8')}")
                message_dict = json.loads(message.value().decode('utf-8'))
                sent_id = message_dict['product']['id']
                message_fix = ShopProductEvent.model_validate_json(message.value())
              
                print("FIX1:", message_fix)
          
                print("FIX:", message_fix.model_dump_json())
                print(message_fix.type)
                message_fix.product.id= sent_id
               
                new_event : ShopProductEvent = ShopProductEvent(type=message_fix.type, product=message_fix.product)

                return JSONResponse (
                   content=new_event.dict()    
                )
             

                # Append the created class to the messages list
    

            except Exception as e:
                print(f"Error occurred while creating ShopProductEvent instance: {e}")
            

            return JSONResponse (message_fix)
        print("All messages consumed.")
        

    except Exception as e:
        logger.error(f"Error occurred while subscribing to messages: {e}")
        raise HTTPException(status_code=500, detail=f"Error occurred while subscribing to messages: {e}")

    finally:
        # Close consumer
        consumer.close()

