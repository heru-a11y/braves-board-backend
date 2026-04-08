from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class CustomException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"errors": exc.message}
    )

def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"errors": str(exc.detail)}
    )

def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = "Format input tidak valid"
    if len(exc.errors()) > 0:
        error_msg = f"{exc.errors()[0]['loc'][-1]}: {exc.errors()[0]['msg']}"
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": error_msg}
    )

def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"errors": "Terjadi kesalahan internal pada server"}
    )