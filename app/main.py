from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, redis_client
from app.middlewares.cors import setup_cors
from app.exceptions.setup import setup_exception_handlers
from app.api.v1 import auth_routes, board_routes, column_routes, subtasks_routes, task_attachments_routes, task_comments_routes, tasks_routes, time_tracking_routes, daily_cleanup_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()
    await redis_client.close()

app = FastAPI(
    title="Braves Board API",
    version="1.0.0",
    lifespan=lifespan,
)

setup_cors(app)
setup_exception_handlers(app)

app.include_router(auth_routes.router)
app.include_router(board_routes.router)
app.include_router(column_routes.router)
app.include_router(tasks_routes.router)
app.include_router(subtasks_routes.router)
app.include_router(task_comments_routes.router)
app.include_router(task_attachments_routes.router)
app.include_router(task_attachments_routes.attachments_router)
app.include_router(time_tracking_routes.router)
app.include_router(daily_cleanup_routes.router)