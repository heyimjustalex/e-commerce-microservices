from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from app.middlewares.authorization_middleware import AuthorizationMiddleware
from app.exceptions.handlers import *
from app.exceptions.definitions import *
from app.controllers.gateway_controller import router

authorization_middleware:AuthorizationMiddleware = AuthorizationMiddleware()
app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=authorization_middleware)
app.add_exception_handler(TokenInvalid,token_invalid_exception_handler)
app.add_exception_handler(NoAccessToResource,no_access_to_resource_exception_handler)
app.add_exception_handler(TokenExpired,token_expired_exception_handler)
app.include_router(router)


 

