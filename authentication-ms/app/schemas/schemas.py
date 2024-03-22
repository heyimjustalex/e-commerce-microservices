from pydantic import BaseModel

class UserCreateRequest(BaseModel):
    email:str
    password:str

class UserLoginRequest(BaseModel):
    email:str
    password:str
    
class UserRegisterResponse(BaseModel):
    email: str
    role: str

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
   


