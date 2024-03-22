
import re
from app.repositories.user_repository import UserRepository
from app.models.models import User
from hashlib import sha256
from app.schemas.schemas import UserRegisterRequest
from app.exceptions.definitions import UserAlreadyExists, UserEmailIncorrectFormat, UserInvalidCredentials
from typing import Union

email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

def is_email_valid(email: str) -> bool:
    if re.fullmatch(email_regex, email):
        return True
    else:
        return False

class UserService:
    def __init__(self, repository:UserRepository) -> None:
        self.repository: UserRepository = repository

    def create_user(self, data:UserRegisterRequest, role:str) -> User:
        email :str = data.email
        password : str = data.password
        if not is_email_valid(data.email):
            raise UserEmailIncorrectFormat()
        if self.repository.get_user_by_email(email):
            raise UserAlreadyExists()
            
        password_hash: str = sha256(password.encode('utf-8')).hexdigest()
        user:User = User(email=email,password_hash=password_hash, role=role)   
        user = self.repository.create_user(user)
        return user
    
    def check_user_credentials(self, email:str, password:str) -> User:
        if not is_email_valid(email):
            raise UserEmailIncorrectFormat()
        
        user:Union[User,None] = self.repository.get_user_by_email(email)
        
        if not user:
            raise UserInvalidCredentials()
        if sha256(password.encode('utf-8')).hexdigest() != user.password_hash:
            raise UserInvalidCredentials()
        return user

    def check_user_exists(self,email) -> User:     
        if not is_email_valid(email):
            raise UserEmailIncorrectFormat()
        
        user:Union[User,None] = self.repository.get_user_by_email(email)
        if not user:
            raise UserInvalidCredentials()    
        return user
  
    

