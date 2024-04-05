from fastapi.responses import JSONResponse, Response
from fastapi import  Request
from app.exceptions.definitions import *

async def product_incorrect_format_exception_handler(request: Request, exc:ProductIncorrectFormat):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def product_already_exists_exception_handler(request: Request, exc:ProductAlreadyExists):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def product_not_found_exception_handler(request: Request, exc:ProductNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )


async def product_quantity_bad_exception_handler(request: Request, exc:ProductQuantityBad):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def orders_not_found_exception_handler(request: Request, exc:OrdersNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def orders_incorrect_format_exception_handler(request: Request, exc:OrdersIncorrectFormat):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def orders_placing_failed_exception_handler(request: Request, exc:OrderPlacingFailed):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def invalid_token_format_exception_handler(request: Request, exc:InvalidTokenFormat):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def invalid_token_email_exception_handler(request: Request, exc:InvalidTokenEmail):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def category_not_found_exception_handler(request: Request, exc:CategoryNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def broker_message_publish_exception_handler(request: Request, exc:BrokerMessagePublishError):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

    