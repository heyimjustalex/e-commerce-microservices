
import re
from pymongo.database import Database
from app.repositories.user_repository import UserRepository
from app.models.models import User
from hashlib import sha256
from app.exceptions.definitions import UserAlreadyExists, IncorrectEmailFormat
from fastapi import status, HTTPException

email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def is_email_valid(email: str) -> bool:
    if re.fullmatch(email_regex, email):
        return True
    else:
        return False

class UserService:
    def __init__(self, db:Database) -> None:
        self.repostiory: UserRepository = UserRepository(db)

    def create_user(self, email:str, password:str) -> None:
        if not is_email_valid(email):
            raise IncorrectEmailFormat(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="This e-mail is not acceptable")
        if self.repostiory.get_user_by_email(email):
            raise UserAlreadyExists(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="This e-mail is not acceptable")
            
        password_hash: str = sha256(password.encode('utf-8')).hexdigest()
        user:User = User(email=email,password_hash=password_hash)
        self.repostiory.create_user(user)

  
    

