from fastapi import FastAPI
from exceptions.handlers import *
from exceptions.definitions import *
from controllers.auth_controller import router as user_router
import sys

app = FastAPI()
app.add_exception_handler(UserAlreadyExists,user_already_exists_exception_handler)
app.add_exception_handler(UserEmailIncorrectFormat,user_register_email_bad_format_exception_handler)
app.include_router(user_router)
 