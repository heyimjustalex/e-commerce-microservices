from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from app.models.models import User
from typing import Any, Dict, Union


class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db: Database = db
        self.users: Collection = self.db['users']

    def create_user(self, user: User) -> None:
        user_dict: Dict[str, Any] = user.model_dump()
        self.users.insert_one(user_dict)

    def get_user_by_email(self,email) -> Union[User, None]:
        user_data: Union[User, None]  = self.users.find_one({"email": email})
        if user_data:
            return User(**user_data)
        return None

