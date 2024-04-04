from fastapi import Request,status
from fastapi.datastructures import QueryParams
from fastapi.responses import JSONResponse
import httpx
from fastapi import APIRouter
from fastapi import Request
from app.exceptions.definitions import *
from app.exceptions.handlers import *
from app.services.gateway_service import GatewayService
from app.const.const import endpoint_redirect_map
import json

router = APIRouter(
    tags=['gateway']
)

gateway_service : GatewayService = GatewayService() 

@router.get("/api/orders")
async def get_orders(request:Request):
   path: str = request.url.path
   gateway_service.verify_request(request)
   email  = gateway_service.get_email_from_jwt_params(request)
   backend_service_url: str = endpoint_redirect_map[path]

   params : QueryParams = QueryParams({'email':email})



   try:
        async with httpx.AsyncClient() as client:      
            response: httpx.Response = await client.get(backend_service_url + path,params=params)
        return JSONResponse(status_code=response.status_code,content=response.json())
   except Exception as exc:
         return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={'detail':exc})

@router.post("/api/orders")
async def post_orders(request:Request):
   path: str = request.url.path
   gateway_service.verify_request(request)
   email  = gateway_service.get_email_from_jwt_params(request)
   backend_service_url: str = endpoint_redirect_map[path]
   body: bytes  = await request.body()   
   json_body : dict[str,str] = json.loads(body)
   json_body['email'] = email
 
   try:
        async with httpx.AsyncClient() as client:      
            response: httpx.Response = await client.post(backend_service_url + path,json=json_body)
        return JSONResponse(status_code=response.status_code,content=response.json())
   except Exception as exc:
         return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={'detail':exc})



@router.get("/{path:path}")
async def get_gateway(request:Request):
    gateway_service.verify_request(request)

    path: str = request.url.path
    params: QueryParams = request.query_params    
    backend_service_url: str = endpoint_redirect_map[path]

    try:
        async with httpx.AsyncClient() as client:      
            response = await client.get(backend_service_url + path,params=params)
        
            return JSONResponse(status_code=response.status_code,content=response.json())
    except Exception as exc:
         return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={'detail':exc})
    
@router.post("/{path:path}")
async def post_gateway(request:Request):
    gateway_service.verify_request(request)
    path: str = request.url.path
    body: bytes  = await request.body()
    json_body : dict[str,str] = json.loads(body)

    backend_service_url: str = endpoint_redirect_map[path]

    try:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.post(backend_service_url + path, json=json_body)
            return JSONResponse(status_code=response.status_code,content=response.json())
    except:
         return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={'detail':"Service unavaliable!"})
