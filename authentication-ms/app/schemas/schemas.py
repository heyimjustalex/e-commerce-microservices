from pydantic import BaseModel

class UserRegisterRequest(BaseModel):
    email:str
    password:str

class UserLoginRequest(BaseModel):
    email:str
    password:str

class RefreshTokenRequest(BaseModel):
    refresh_token:str
    
class UserRegisterResponse(BaseModel):
    email: str
    role: str

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    access_token:str
   


