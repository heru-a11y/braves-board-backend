from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.exceptions.base_exceptions import CustomException


def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": exc.__class__.__name__,
                "message": exc.message,
                "request_id": None,
            },
        },
    )


def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "HTTP_EXCEPTION",
                "message": str(exc.detail),
                "request_id": None,
            },
        },
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = "Format input tidak valid"

    if len(exc.errors()) > 0:
        message = f"{exc.errors()[0]['loc'][-1]}: {exc.errors()[0]['msg']}"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": message,
                "request_id": None,
            },
        },
    )


def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Terjadi kesalahan internal pada server",
                "request_id": None,
            },
        },
    )