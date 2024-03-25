from datetime import datetime, timezone
import os
from typing import Union, Any
from fastapi import Request
import jwt
from app.exceptions.definitions import *
from app.exceptions.handlers import *
from starlette.types import Message

# If endpoint not specified, then allowed by default
ENDPOINT_ACCESS_MAP: dict[tuple[str,str,str],bool] = {
    #    ENDPOINT   HTTP_VERB  ROLE
    ("/api/products", "POST", "user"): False,
    ("/api/products", "POST", "visitor"): False,
}

class AuthorizationMiddleware:
    def __init__(self) -> None:
        self.JWT_ACCESS_TOKEN_SECRET_KEY: Union[str, None] = os.getenv('JWT_ACCESS_TOKEN_SECRET_KEY')        
        self.JWT_TOKEN_ALG: Union[str, None] = os.getenv('JWT_TOKEN_ALG')

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    def get_role_from_token(self, access_token: str) -> str:
        if not self.JWT_ACCESS_TOKEN_SECRET_KEY or not self.JWT_TOKEN_ALG:
            raise TokenInvalid()        
              
        decoded_jwt: dict[str, Any] = jwt.decode(access_token, str(self.JWT_ACCESS_TOKEN_SECRET_KEY), [str(self.JWT_TOKEN_ALG)])
        email: str = decoded_jwt['email']
        role: str = decoded_jwt['role']
        exp: float = decoded_jwt['exp']
        if not email or not role or not exp:
            raise TokenInvalid()
        expiration_time: datetime = datetime.fromtimestamp(exp).replace(tzinfo=timezone.utc)
        if expiration_time < datetime.now(timezone.utc):
            raise TokenInvalid()
        return role                


    def determine_request_access(self, path: str, method: str, role: str) -> bool:
   
        map_key: tuple[str, str, str] = (path.lower(), method.upper(), role.lower())
        if map_key not in ENDPOINT_ACCESS_MAP:
            return True
        return ENDPOINT_ACCESS_MAP[map_key]

    async def __call__(self, request: Request, call_next):
        # Known starlette bug
        # https://github.com/tiangolo/fastapi/issues/394
        await self.set_body(request)
        body = await request.body()
        # end of bug fix
        try:
            path: str = request.url.path
            method: str = request.method
            role: str = "visitor"
            try:
                body = await request.json()  
            except:
                body = None
            if body:               
                token: Union[str, None] = body.get("access_token")
                if token:
                    role = self.get_role_from_token(token)
    

            access_to_endpoint: bool = self.determine_request_access(path, method, role)

            if not access_to_endpoint:   
                raise NoAccessToResource()      
            
           
            
        except Exception as exc:  
            if isinstance(exc, NoAccessToResource) or isinstance(exc, TokenInvalid):
                    return JSONResponse(status_code=exc.status_code, content={'detail':exc.detail})
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail':"Bad request!"})
        

        response = await call_next(request) 
        return response     