from fastapi import FastAPI, HTTPException
from confluent_kafka import Producer, Consumer, KafkaError
import json
import logging
import time
app = FastAPI()
from pymongo import MongoClient
from pymongo.errors import OperationFailure

uri = "mongodb://root:root@products-db:27017"
print("DUPA")
# Connect to MongoDB
client = MongoClient(uri)

# Access a database
db = client["shop"]

# Access a collection
collection = db["products"]

# Start a session
with client.start_session() as session:
    # Start a transaction
    with session.start_transaction():
        try:
            # Perform operations within the transaction
            # For example, insert a document into the collection
            test = {'key':'OMFG2'}
            print(test)
            collection.insert_one(test, session=session)
          #  raise OperationFailure("Test transaction rollbac k")
            
            # If an error occurs, raise an exception to roll back the transaction
            # For testing purposes, let's raise an OperationFailure


            # If no exception is raised, commit the transaction
            session.commit_transaction()
        except OperationFailure as e:
            # If an OperationFailure occurs, the transaction will be aborted
            print(f"Transaction failed: {e}")
            session.abort_transaction()

# Close the MongoDB connection
client.close()

