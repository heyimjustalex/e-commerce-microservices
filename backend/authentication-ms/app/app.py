from fastapi import FastAPI
from app.exceptions.handlers import *
from app.exceptions.definitions import *
from app.controllers.authentication_controller import router as user_router

import time
time.sleep(6)

app = FastAPI()
app.add_exception_handler(UserAlreadyExists,user_already_exists_exception_handler)
app.add_exception_handler(UserEmailIncorrectFormat,user_register_email_bad_format_exception_handler)
app.add_exception_handler(UserInvalidCredentials,user_invalid_credentials_exception_handler)
app.add_exception_handler(RefreshTokenInvalid,refreshing_token_bad_format_exception_handler)

app.include_router(user_router)
