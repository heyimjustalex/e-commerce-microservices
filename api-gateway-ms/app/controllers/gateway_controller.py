from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import httpx
from typing import Optional
from  httpx import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.middlewares.authorization_middleware import AuthorizationMiddleware
from fastapi import APIRouter
import os

router = APIRouter(
    tags=['gateway']
)
# Define mappings from gateway endpoints to backend services
ENDPOINT_MAP: dict[str, str] = {
    "/api/products": "http://products-ms:8000",  
    "/api/products/category": "http://products-ms:8000",  
    "/api/register": "http://authentication-ms:8000",
    "/api/login": "http://authentication-ms:8000",
    "/api/refresh": "http://authentication-ms:8000",
}

@router.get("/{path:path}")
async def gateway(path: str, name: Optional[str] = None):
    path = "/"+path
    if path not in ENDPOINT_MAP:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    backend_service_url = ENDPOINT_MAP[path]
    try:
        async with httpx.AsyncClient() as client:
            if name is not None:
                response = await client.get(backend_service_url + path, params={"name": name})
            else:
                response = await client.get(backend_service_url + path)
            return JSONResponse(status_code=response.status_code,content=response.json())
    except:
         return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={'detail':"Service unavaliable!"})
@router.post("/{path:path}")
async def post_gateway(path: str, data:dict):
    path = "/"+path
    if path not in ENDPOINT_MAP:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    backend_service_url: str = ENDPOINT_MAP[path]
    
    try:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.post(backend_service_url + path, json=data)
            return JSONResponse(status_code=response.status_code,content=response.json())
    except:
         return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={'detail':"Service unavaliable!"})
