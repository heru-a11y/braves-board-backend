from fastapi import FastAPI

from app.api.main import api_router
from app.observability.middleware import setup_prometheus
from app.observability.metrics import metrics_endpoint
from app.api.health.views import router as health_router

from app.middleware.cors import setup_cors
from app.middleware.request_id import setup_request_id
from app.middleware.access_log import setup_access_log
from app.middleware.rate_limit import setup_rate_limit
from app.middleware.security_headers import setup_security_headers
from app.api.exceptions.setup_exceptions import setup_exception_handlers

app = FastAPI()

setup_cors(app)
setup_security_headers(app)
setup_rate_limit(app)
setup_access_log(app)
setup_request_id(app) 

setup_exception_handlers(app)

setup_prometheus(app)
app.add_api_route("/metrics", metrics_endpoint, methods=["GET"])
app.include_router(health_router)

app.include_router(api_router)