from fastapi import FastAPI
from app.exceptions.handlers import *
from app.exceptions.definitions import *
from app.controllers.gateway_controller import router


app = FastAPI()

app.add_exception_handler(TokenInvalid,token_invalid_exception_handler)
app.add_exception_handler(TokenExpired,token_expired_exception_handler)
app.add_exception_handler(NoAccessToResource,no_access_to_resource_exception_handler)
app.add_exception_handler(EndpointNotFound,endpoint_not_found_exception_handler)
app.include_router(router)



 

