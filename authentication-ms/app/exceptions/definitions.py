from fastapi import HTTPException
from fastapi import status, HTTPException

class UserAlreadyExists(HTTPException):
    def __init__(self, status_code: int =status.HTTP_400_BAD_REQUEST, detail: str = "This e-mail is not acceptable"):
        super().__init__(status_code=status_code, detail=detail)

class UserEmailIncorrectFormat(HTTPException):
    def __init__(self, status_code: int =status.HTTP_400_BAD_REQUEST, detail: str = "This e-mail is not acceptable"):
        super().__init__(status_code=status_code, detail=detail)

class UserInvalidCredentials(HTTPException):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: str="Incorrect e-mail or password"):
        super().__init__(status_code=status_code, detail=detail)

class RefreshTokenInvalid(HTTPException):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED, detail: str="Incorrect token"):
        super().__init__(status_code=status_code, detail=detail)
      