from fastapi.responses import JSONResponse
from fastapi import  Request
from app.exceptions.definitions import *

async def token_invalid_exception_handler(request: Request, exc:TokenInvalid):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def no_access_to_resource_exception_handler(request: Request, exc:NoAccessToResource):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def token_expired_exception_handler(request: Request, exc:NoAccessToResource):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

async def endpoint_not_found_exception_handler(request: Request, exc:EndpointNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':exc.detail}
    )

