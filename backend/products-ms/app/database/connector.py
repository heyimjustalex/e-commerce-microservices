import os
from pymongo import MongoClient
from pymongo.database import Database
from typing import Union

class Connector:
    _client: Union[MongoClient, None]  = None 
    hostname : Union[str, None] = os.getenv('DB_HOSTNAME')
    username : Union[str, None]  = os.getenv('DB_USERNAME')
    password : Union[str, None]  = os.getenv('DB_PASSWORD')
    db_name:  Union[str, None]  = os.getenv('DB_NAME')
    port: int = int(os.getenv('DB_PORT', '999999')) 

    @classmethod
    def get_db_client(cls) -> MongoClient:
        if not cls._client:
            cls._client =  MongoClient(host=cls.hostname,port=cls.port,username=cls.username,password=cls.password)
        return cls._client            

    @classmethod
    def get_db(cls) -> Database: 
        return cls.get_db_client().get_database(cls.db_name)
    



