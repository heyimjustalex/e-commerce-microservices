from fastapi import HTTPException
from fastapi import status, HTTPException

class ProductIncorrectFormat(HTTPException):
    def __init__(self, status_code: int =status.HTTP_400_BAD_REQUEST, detail: str = "Product format is not acceptable"):
        super().__init__(status_code=status_code, detail=detail)

class ProductAlreadyExists(HTTPException):
    def __init__(self, status_code: int =status.HTTP_400_BAD_REQUEST, detail: str = "Product already exists"):
        super().__init__(status_code=status_code, detail=detail)

class ProductNotFound(HTTPException):
    def __init__(self, status_code: int =status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail="The requested product does not exist.")

class CategoryNotFound(HTTPException):
    def __init__(self, status_code: int =status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail="The requested category does not exist.")