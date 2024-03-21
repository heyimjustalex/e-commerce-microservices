from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult
from app.models.models import User
from typing import Any, Dict, Union

class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db: Database = db
        self.users: Collection = self.db['users']

    def create_user(self, user: User) -> User:
        user_dict: Dict[str, Any] = user.model_dump()
        id: InsertOneResult = self.users.insert_one(user_dict)
        user._id = id.inserted_id
        return user


    def get_user_by_email(self,email:str) -> Union[User, None]:
        user: Union[User, None]  = self.users.find_one({"email": email})
        if not user:
            return None
        return User(**user)
     
            
       
