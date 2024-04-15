
# Define mappings from gateway endpoints to backend services
endpoint_redirect_map: dict[str, str] = {
        "/api/products": "http://products-ms:8000",  
        "/api/categories": "http://products-ms:8000",  
        "/api/register": "http://authentication-ms:8000",
        "/api/login": "http://authentication-ms:8000",
        "/api/refresh": "http://authentication-ms:8000",
        "/api/orders":"http://orders-ms:8000",
        "/api/products_error":"http://products-ms:8000",  
        "/api/authentication_error":"http://authentication-ms:8000",  
        "/api/orders_error":"http://orders-ms:8000",  
    }

endpoint_access_map: dict[tuple[str,str,str],bool] = {
            # If not listed access is allowed
            #    ENDPOINT   HTTP_VERB  ROLE
            ("/api/products", "POST", "user"): False,
            ("/api/products", "POST", "visitor"): False,
            ("/api/orders", "GET", "visitor"): False,
            ("/api/orders", "POST", "visitor"): False,}