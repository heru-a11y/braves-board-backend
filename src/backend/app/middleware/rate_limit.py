# type: ignore
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.connections.redis import redis_client


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit=120, window=60):
        super().__init__(app)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next):
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            ip = forwarded_for.split(",")[0].strip()
        else:
            ip = request.client.host 

        key = f"rate_limit:{ip}"
        now_timestamp = time.time()
        member_id = f"{now_timestamp}:{uuid.uuid4().hex}"

        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.zremrangebyscore(key, 0, now_timestamp - self.window)
            pipe.zadd(key, {member_id: now_timestamp})
            pipe.zcard(key)
            pipe.expire(key, self.window)

            results = await pipe.execute()

        count = results[2]

        if count > self.limit:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED", 
                        "message": "Terlalu banyak permintaan. Silakan coba lagi nanti."
                    }
                },
            )

        return await call_next(request)


def setup_rate_limit(app):
    app.add_middleware(RateLimitMiddleware)