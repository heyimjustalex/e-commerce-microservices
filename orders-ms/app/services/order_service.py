
import re
from ..models.models import Product
from app.repositories.order_repository import OrderRepository
from app.schemas.schemas import OrderCreateRequest, OrdersRequest
from app.exceptions.definitions import ProductQuantityBad, InvalidTokenFormat, ProductNotFound,OrdersIncorrectFormat, OrdersNotFound,CategoryNotFound, ProductNotFound, ProductAlreadyExists, ProductIncorrectFormat
from typing import Union, List, Tuple, Any
from app.models.models import Order, PyObjectId, BuyProductItem
from app.repositories.product_repository import ProductRepository
import jwt
import os

class OrderService:
    def __init__(self, order_repository: OrderRepository, product_repository:ProductRepository) -> None:
        self.order_repository: OrderRepository = order_repository
        self.product_repository: ProductRepository = product_repository
        self.JWT_ACCESS_TOKEN_SECRET_KEY : Union[str, None]  = os.getenv('JWT_ACCESS_TOKEN_SECRET_KEY')
        self.JWT_REFRESH_TOKEN_SECRET_KEY : Union[str, None]  = os.getenv('JWT_REFRESH_TOKEN_SECRET_KEY')
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES : int = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES',7*24*60))
        self.JWT_TOKEN_ALG : Union[str, None] = os.getenv('JWT_TOKEN_ALG')

    def _get_verified_create_request_params(self,data:OrderCreateRequest) -> Tuple[str,str]:
        try:
            decoded_jwt:dict[str,Any]= jwt.decode(data.access_token,str(self.JWT_ACCESS_TOKEN_SECRET_KEY),[str(self.JWT_TOKEN_ALG)])
            email:str = decoded_jwt['email']
            role:str = decoded_jwt['role']     
            if not role or role.lower() != "user" or not email:
                raise OrdersIncorrectFormat()

        except:
            raise InvalidTokenFormat()        
        return (email,role)

    def _get_verified_get_request_params(self,data:OrdersRequest) -> Tuple[str,str]:
        try:
            decoded_jwt:dict[str,Any]= jwt.decode(data.access_token,str(self.JWT_ACCESS_TOKEN_SECRET_KEY),[str(self.JWT_TOKEN_ALG)])
            email:str = decoded_jwt['email']
            role:str = decoded_jwt['role']     
            if not role or role.lower() != "user" or not email:
                raise OrdersIncorrectFormat()

        except:
            raise InvalidTokenFormat()        
        return (email,role)
    
    
    def _verify_create_request_format(self, data: OrderCreateRequest):
        bought_products: List[BuyProductItem] = data.products

        if bought_products is None :
            raise ValueError("No products provided.")

        for product in bought_products:
            if product is None:
                raise OrdersIncorrectFormat()
            if not isinstance(product, BuyProductItem):
                raise OrdersIncorrectFormat()
            if not isinstance(product.name, str) or not re.match(r'^[a-zA-Z0-9\s]+$', product.name):
                raise OrdersIncorrectFormat()
            if not isinstance(product.quantity, int) or product.quantity <= 0:
                raise OrdersIncorrectFormat()

    def get_orders_by_email(self, data:OrdersRequest) -> List[Order]:        
        params : Tuple[str,str] = self._get_verified_get_request_params(data)
        orders: Union[List[Order],None] = self.order_repository.get_orders_by_email(params[0])        
       
        if not orders:
            raise OrdersNotFound()
        return orders   
    
    def _calculate_order_cost(self, products:List[BuyProductItem])->float:
        order_cost:float = 0
        for product in products:
            prod_got_by_name: Product | None = self.product_repository.get_product_by_name(product.name)
            if not prod_got_by_name:
                raise ProductNotFound()
            order_cost+=prod_got_by_name.price * product.quantity
            product.price = prod_got_by_name.price
        return order_cost
    
    def _check_products_existance_and_quantity(self,products:List[BuyProductItem]):
        for product in products:
            prod_got_by_name: Product | None = self.product_repository.get_product_by_name(product.name)
            if not prod_got_by_name:
                raise ProductNotFound()
                      
            if prod_got_by_name.quantity < product.quantity:
                raise ProductQuantityBad()
        
            

    def create_order(self, data:OrderCreateRequest) -> Order:
        self._verify_create_request_format(data)               
        params : Tuple[str,str] = self._get_verified_create_request_params(data)
        email : str = params[0]
        products: List[BuyProductItem] = [BuyProductItem(name=product.name.lower(), price=product.price, quantity=product.quantity) for product in data.products]  
        self._check_products_existance_and_quantity(products)
        order_cost:float = self._calculate_order_cost(products)    


        order : Order = Order(client_email=email.lower(),cost=order_cost, status="PENDING", products=products)
        created_order: Order = self.order_repository.create_order(order)

        return created_order

