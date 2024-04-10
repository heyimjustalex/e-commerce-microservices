from fastapi import status
from fastapi import status, HTTPException

class TokenInvalid(HTTPException):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: str="Incorrect token"):
        super().__init__(status_code=status_code, detail=detail)

class TokenExpired(HTTPException): 
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: str="Token expired"):
        super().__init__(status_code=status_code, detail=detail)

class NoAccessToResource(HTTPException):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: str="You have no access to this resource!"):
        super().__init__(status_code=status_code, detail=detail)

class EndpointNotFound(HTTPException):
    def __init__(self, status_code: int = status.HTTP_404_NOT_FOUND, detail: str="Endpoint not found!"):
        super().__init__(status_code=status_code, detail=detail)
      