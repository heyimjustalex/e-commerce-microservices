from fastapi.responses import JSONResponse
from fastapi import  Request
from app.exceptions.definitions import *


async def user_already_exists_exception_handler(request: Request, exc:UserAlreadyExists):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def user_register_email_bad_format_exception_handler(request: Request, exc:UserEmailIncorrectFormat):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def refreshing_token_bad_format_exception_handler(request: Request, exc:RefreshTokenInvalid):
    return JSONResponse(   
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )
    
async def user_invalid_credentials_exception_handler(request: Request, exc:UserInvalidCredentials):
    return JSONResponse(   
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )
    

    
    