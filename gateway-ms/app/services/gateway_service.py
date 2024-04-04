from fastapi.datastructures import QueryParams
from app.exceptions.definitions import *
from app.exceptions.handlers import *
from typing import Union, Any
import os
import jwt
from datetime import datetime, timezone
from fastapi import Request
from app.const.const import endpoint_redirect_map, endpoint_access_map

class GatewayService:
    def __init__(self) -> None:
        self.JWT_ACCESS_TOKEN_SECRET_KEY: Union[str, None] = os.getenv('JWT_ACCESS_TOKEN_SECRET_KEY')        
        self.JWT_TOKEN_ALG: Union[str, None] = os.getenv('JWT_TOKEN_ALG')   

    def _determine_request_access(self, path: str, method: str, role: str) -> bool:
        map_key: tuple[str, str, str] = (path.lower(), method.upper(), role.lower())
        
        if map_key not in endpoint_access_map:
            print("MAP KEY", map_key)
            return True
        return endpoint_access_map[map_key]

    def _get_role_email_tuple_from_token(self, access_token: str) -> tuple[str,str]:
        if not self.JWT_ACCESS_TOKEN_SECRET_KEY or not self.JWT_TOKEN_ALG:
          
            raise TokenInvalid()        
        try:    
            decoded_jwt: dict[str, Any] = jwt.decode(access_token, str(self.JWT_ACCESS_TOKEN_SECRET_KEY), [str(self.JWT_TOKEN_ALG)])
        except:
            raise TokenInvalid()
        email: str = decoded_jwt['email']
        role: str = decoded_jwt['role']
        exp: float = decoded_jwt['exp']
        if not email or not role or not exp:
            
            raise TokenInvalid()
       
        
        expiration_time: datetime = datetime.fromtimestamp(exp).replace(tzinfo=timezone.utc)
        if expiration_time < datetime.now(timezone.utc):
            raise TokenInvalid()
        return role, email         
    
    def verify_request(self, request:Request):
        print("DUPA")
        path: str = request.url.path

        if path not in endpoint_redirect_map:
            raise EndpointNotFound()

        method:str = request.method
        token: str | None = request.headers.get('Authorization')

        role:str = "visitor"

        if token:
            token = token[len('Bearer '):]
            role_email_pair : tuple[str,str] = self._get_role_email_tuple_from_token(token)
            print(role_email_pair)
            role = role_email_pair[0]
        
        has_valid_access:bool = self._determine_request_access(path,method,role)
        if not has_valid_access:
            raise NoAccessToResource()
    
    def get_email_from_jwt_params(self,request:Request) -> str:
        token: str | None = request.headers.get('Authorization')
        if not token:
            raise NoAccessToResource()
        token = token[len('Bearer '):]
        role_email_pair : tuple[str,str] = self._get_role_email_tuple_from_token(token)
        return role_email_pair[1]

    


        
        
            
        


