# type: ignore
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.base import CustomException
from app.exceptions.global_exception import (
    custom_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler
)

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)