from fastapi import FastAPI
from app.exceptions.definitions import *
from app.exceptions.handlers import *
from app.controllers.auth_controller import router as user_router
 
app = FastAPI()
app.add_exception_handler(UserAlreadyExists,user_already_exists_exception_handler)
app.include_router(user_router)
 