from fastapi import FastAPI, HTTPException
from confluent_kafka import Producer, Consumer, KafkaError
import json
import logging
import time
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = 'message-broker:19092'
KAFKA_TOPIC = 'test_topic'


def kafka_consumer():
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'earliest'
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
        producer.produce(KAFKA_TOPIC, json.dumps(message))
        # Flush producer to ensure message is sent
        producer.flush()
        return {"message": "Message published successfully"}
    except KafkaError as e:
        raise HTTPException(status_code=500, detail=f"Error publishing message to Kafka: {e}")



@app.get("/subscribe/")
async def subscribe_messages():
    # Initialize Kafka consumer
    consumer = kafka_consumer()

    # Subscribe to Kafka topic
    consumer.subscribe([KAFKA_TOPIC])

    messages = []


    while True:
        try: 
            message = consumer.poll(10.0)

            if not message:
                time.sleep(120) # Sleep for 2 minutes

            if message.error():
                print(f"Consumer error: {message.error()}")
                continue

            print(f"Received message: {message.value().decode('utf-8')}")
        except:
            pass

        finally:
            consumer.close()
            print("Goodbye")


