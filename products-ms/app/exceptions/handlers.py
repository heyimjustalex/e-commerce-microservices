from fastapi.responses import JSONResponse, Response
from fastapi import  Request
from app.exceptions.definitions import *

async def product_already_exists_exception_handler(request: Request, exc:ProductAlreadyExists):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def product_incorrect_format_exception_handler(request: Request, exc:ProductIncorrectFormat):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def product_not_found_exception_handler(request: Request, exc:ProductNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def category_not_found_exception_handler(request: Request, exc:CategoryNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

  

    