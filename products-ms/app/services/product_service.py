
import re
from aiokafka import AIOKafkaProducer
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.schemas import ProductCreateRequest, ProductItem
from app.exceptions.definitions import BrokerMessagePublishError,ProductCreationFailed, CategoryNotFound, ProductNotFound, ProductAlreadyExists, ProductIncorrectFormat
from typing import Union, List, Tuple
from app.models.models import Product, Category, PyObjectId, ShopProductEvent
from pymongo import MongoClient
from app.brokers.producers.producer import MessageProducer

class ProductService:
    def __init__(self, product_repository: ProductRepository,category_repository:CategoryRepository) -> None:
        self.product_repository: ProductRepository = product_repository
        self.category_repository:CategoryRepository = category_repository


    def check_product_format(self, product:Product):
        if not re.match(r'^[a-zA-Z\s]+$', product.name):
            raise ProductIncorrectFormat(detail="Name should contain only letters and spaces")

        if not re.match(r'^[a-zA-Z\s]+$', product.description):
            raise ProductIncorrectFormat(detail="Description should contain only letters and spaces")

        if not isinstance(product.price, float):
            raise ProductIncorrectFormat(detail="Price should be a float")

        if product.price < 0:
            raise ProductIncorrectFormat(detail="Price should be a positive value")
        if not isinstance(product.quantity,int):
            raise ProductIncorrectFormat(detail="Quantity should be an int")

        return True

    def get_products(self) -> List[Product]:
        products: List[Product] =self.product_repository.get_products()        
        for product in products:
            temp_categories : List[PyObjectId] = []

            for category_id in product.categories:
                category:Union[Category, None] = self.category_repository.get_category_by_id(category_id)
                if category:
                    category_name : str = category.name
                    temp_categories.append(category_name)              
            product.categories = temp_categories

        return products

    def get_product_by_name(self, name:str) -> Product:
        product : Union[Product, None] = self.product_repository.get_product_by_name(name)
        if not product:
           raise ProductNotFound()
        named_categories : List[PyObjectId] = []

        for category_id in product.categories:
            category:Union[Category, None] = self.category_repository.get_category_by_id(category_id)
            if category:
                category_name : str = category.name
                named_categories.append(category_name)   
        product.categories = named_categories     
        return product
        
    def get_products_by_category(self, category_name: str) -> List[Product]:
        category: Category | None = self.category_repository.get_category_by_name(category_name)
        if not category:
            raise CategoryNotFound()
        
        products: List[Product] | None = self.product_repository.get_products_of_category(category.id)
        if not products:
            return []
        
        for product in products:
            temp_categories : List[PyObjectId] = []

            for category_id in product.categories:
                category:Union[Category, None] = self.category_repository.get_category_by_id(category_id)
                if category:
                    temp_name : str = category.name
                    temp_categories.append(temp_name)              
            product.categories = temp_categories     
       
        return products
    
    async def _publish_ProductCreateEvent_to_broker(self,product:Product) -> None:        
        try:
            create_product_event:ShopProductEvent = ShopProductEvent(type="ProductCreate",product=product)
            message_producer: AIOKafkaProducer = await MessageProducer.get_producer()                    
            await message_producer.send(topic='shop', value=create_product_event.model_dump_json())                   
        except:
            raise BrokerMessagePublishError()
           
           
    async def create_product_with_event_ProductCreate(self, data:ProductCreateRequest):
            client:MongoClient = self.product_repository.get_mongo_client()
            # Helper function for verification 
            prod_tuple:Tuple[Product,List[str]] = self._create_product_helper(data)
            with client.start_session() as session:
                with session.start_transaction():
                    try:                                           
                        product: Product=prod_tuple[0]
                        categories:List[str] = prod_tuple[1]  

                        # Create product and publish an event                           
                        created_product : Product = self.product_repository.create_product(product,session)
                        created_product.categories = categories
                        # await self._publish_ProductCreateEvent_to_broker(product)

                        # Save in local DB
                        session.commit_transaction()    
                        return created_product
                    
                    except Exception as e:                  
                        session.abort_transaction()
                        raise ProductCreationFailed()

    def create_product(self, data:ProductCreateRequest) -> Product:
        product_item : ProductItem = data.product
        name :str = product_item.name.lower()
        description : str = product_item.description
        price : float = product_item.price
        quantity: int = product_item.quantity
        categories: List[str] = [category.lower() for category in product_item.categories]  

        if not name or not description or not price or not categories or not quantity or not price:
            ProductIncorrectFormat()

        if self.product_repository.get_product_by_name(name):
            raise ProductAlreadyExists()
        
        categories_ids:List[str] = []
        for i in categories:
            category:Union[Category,None]= self.category_repository.get_category_by_name(i)
            if not category:
                raise CategoryNotFound()
            categories_ids.append(category.id)

        product : Product = Product(name=name, description=description, price=price,categories=categories_ids, quantity=quantity)
        self.check_product_format(product)

        created_product : Product = self.product_repository.create_product(product)
        created_product.categories = categories

        return created_product

    def _create_product_helper(self, data:ProductCreateRequest) -> Tuple[Product,List[str]]:
        product_item : ProductItem = data.product
        name :str = product_item.name.lower()
        description : str = product_item.description
        price : float = product_item.price
        quantity: int = product_item.quantity
        categories: List[str] = [category.lower() for category in product_item.categories]  

        if not name or not description or not price or not categories or not quantity or not price:
            ProductIncorrectFormat()

        if self.product_repository.get_product_by_name(name):
            raise ProductAlreadyExists()
        
        categories_ids:List[str] = []
        for i in categories:
            category:Union[Category,None]= self.category_repository.get_category_by_name(i)
            if not category:
                raise CategoryNotFound()
            categories_ids.append(category.id)

        product : Product = Product(name=name, description=description, price=price,categories=categories_ids, quantity=quantity)
        self.check_product_format(product)
   
        return product, categories

