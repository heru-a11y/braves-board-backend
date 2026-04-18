# type: ignore
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("access")


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        logger.info(
            f"{request.client.host} - {request.method} {request.url.path} " 
            f"{response.status_code} - {process_time:.2f}ms"
        )

        return response


def setup_access_log(app):
    app.add_middleware(AccessLogMiddleware)