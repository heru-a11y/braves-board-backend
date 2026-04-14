from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, redis_client
from app.middlewares.cors import setup_cors
from app.exceptions.setup import setup_exception_handlers
from app.api.v1 import auth, board, column, tasks, subtasks, task_comments
import app.models


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

app.include_router(auth.router)
app.include_router(board.router)
app.include_router(column.router)
app.include_router(tasks.router)
app.include_router(subtasks.router)
app.include_router(task_comments.router)
