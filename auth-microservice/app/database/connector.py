import os
from pymongo import MongoClient
from pymongo.database import Database
from typing import Any, Union
hostname : Union[str, None] = os.getenv('DB_HOSTNAME')
username : Union[str, None]  = os.getenv('DB_USERNAME')
password : Union[str, None]  = os.getenv('DB_PASSWORD')
db_name:  Union[str, None]  = os.getenv('DB_NAME')
port: int = int(os.getenv('DB_PORT', '27017')) 


class Connector:
    _client: Union[MongoClient, None]  = None

    @classmethod
    def get_db_client(cls) -> MongoClient:
        if not cls._client:
            cls._client =  MongoClient(hostname,port,username=username,password=password)
        return cls._client            

    @classmethod
    def get_db(cls) -> Database: 
        return cls.get_db_client().get_database(db_name)


