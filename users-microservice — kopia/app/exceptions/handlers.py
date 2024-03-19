from fastapi.responses import JSONResponse
from fastapi import  Request
from app.exceptions.definitions import *
async def user_already_exists_exception_handler(request: Request, exc:UserAlreadyExists):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )
