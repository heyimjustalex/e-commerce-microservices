from fastapi import FastAPI
from app.exceptions.handlers import *
from app.exceptions.definitions import *
from app.controllers.products_controller import router as products_router

app = FastAPI()
app.add_exception_handler(ProductAlreadyExists,product_already_exists_exception_handler)
app.add_exception_handler(ProductIncorrectFormat,product_incorrect_format_exception_handler)
app.add_exception_handler(ProductNotFound, product_not_found_exception_handler)
app.add_exception_handler(CategoryNotFound, category_not_found_exception_handler)

app.include_router(products_router)
 