from fastapi import FastAPI
from app.exceptions.handlers import *
from app.exceptions.definitions import *
from app.controllers.auth_controller import router as user_router

app = FastAPI()
app.add_exception_handler(UserAlreadyExists,user_already_exists_exception_handler)
app.add_exception_handler(UserEmailIncorrectFormat,user_register_email_bad_format_exception_handler)
app.include_router(user_router)
 