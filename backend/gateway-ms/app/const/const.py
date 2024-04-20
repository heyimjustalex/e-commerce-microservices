import os
# Define mappings from gateway endpoints to backend services
authentication_service_url:str = os.getenv("AUTHENTICATION_SERVICE_URL", "http://authentication-ms:8000") 
products_service_url:str = os.getenv("PRODUCTS_SERVICE_URL", "http://products-ms:8000") 
orders_service_url:str = os.getenv("ORDERS_SERVICE_URL", "http://orders-ms:8000") 

endpoint_redirect_map: dict[str, str] = {
        "/api/products": products_service_url,  
        "/api/categories": products_service_url, 
        "/api/register": authentication_service_url,
        "/api/login": authentication_service_url,
        "/api/refresh": authentication_service_url,
        "/api/orders":orders_service_url,
        "/api/products_error":products_service_url,  
        "/api/authentication_error":authentication_service_url,  
        "/api/orders_error":orders_service_url,  
    }

endpoint_access_map: dict[tuple[str,str,str],bool] = {
            # If not listed access is allowed
            #    ENDPOINT   HTTP_VERB  ROLE
            ("/api/products", "POST", "user"): False,
            ("/api/products", "POST", "visitor"): False,
            ("/api/orders", "GET", "visitor"): False,
            ("/api/orders", "POST", "visitor"): False,}