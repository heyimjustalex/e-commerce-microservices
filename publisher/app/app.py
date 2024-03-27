from fastapi import FastAPI, HTTPException
from confluent_kafka import Producer, Consumer, KafkaError
import json
import logging

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

    try:
        # Poll Kafka for messages

        msg = consumer.poll(timeout=1.0)

        if msg.error():
            raise HTTPException(status_code=500, detail=f"Kafka Consumer error: {msg.error()}")
        else:
            messages.append(json.loads(msg.value().decode('utf-8')))
            logger.info(f"Received message: {messages[-1]}")
            logger.info("Returning messages...")
            consumer.close()
            return {"messages": messages}

    except Exception as e:
        logger.error(f"Error occurred while subscribing to messages: {e}")
        raise HTTPException(status_code=500, detail=f"Error occurred while subscribing to messages: {e}")
    finally:
        # Close consumer
        consumer.close()


