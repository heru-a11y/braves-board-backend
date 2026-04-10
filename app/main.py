from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, redis_client
from app.middlewares.cors import setup_cors
from app.exceptions.setup import setup_exception_handlers
from app.api.v1 import auth, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()
    await redis_client.close()

app = FastAPI(
    title="Braves Board API",
    version="1.0.0",
    lifespan=lifespan
)

setup_cors(app)
setup_exception_handlers(app)

app.include_router(auth.router)
app.include_router(tasks.router)