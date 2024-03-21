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
    email:str  
    access_token: str
    refresh_token: str
    token_type: str

