from fastapi import HTTPException
from fastapi import status, HTTPException

class ProductIncorrectFormat(HTTPException):
    def __init__(self, status_code: int =status.HTTP_400_BAD_REQUEST, detail: str = "Product format is not acceptable"):
        super().__init__(status_code=status_code, detail=detail)

# Product conflict
class ProductAlreadyExists(HTTPException):
    def __init__(self, status_code: int =status.HTTP_400_BAD_REQUEST, detail: str = "Product already exists"):
        super().__init__(status_code=status_code, detail=detail)

class ProductNotFound(HTTPException):
    def __init__(self, status_code: int =status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail="The requested product does not exist.")

class ProductQuantityBad(HTTPException):
    def __init__(self, status_code: int =status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail="The requested amount does not exist.")

class OrdersNotFound(HTTPException):
    def __init__(self, status_code: int =status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail="No orders found.")

class OrdersIncorrectFormat(HTTPException):
    def __init__(self, status_code: int =status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail="Bad request format")

class OrderPlacingFailed(HTTPException):
    def __init__(self, status_code: int =status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail="Placing order failed, try again later")

class InvalidTokenFormat(HTTPException):
    def __init__(self, status_code: int =status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail="Invalid token format")
        
class InvalidTokenEmail(HTTPException):
    def __init__(self, status_code: int =status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail="Invalid email from JWT token") 

class CategoryNotFound(HTTPException):
    def __init__(self, status_code: int =status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail="The requested category does not exist.")

class BrokerMessagePublishError(HTTPException):
    def __init__(self, status_code: int =status.HTTP_503_SERVICE_UNAVAILABLE):
        super().__init__(status_code=status_code, detail="Broker publish error") 

# Event exceptions

class OrderStatusUpdateFailed(Exception):
    def __init__(self, message="Order status after receiving OrderStatusUpdateEvent failed"):
        super().__init__(message)
        self.message = message

class ProductQuantityUpdateFailed(Exception):
    def __init__(self, message="Product quantity update failed after receiving ProductQuantityUpdateFailed failed"):
        super().__init__(message)
        self.message = message