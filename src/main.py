import contextlib
import logging
from typing import AsyncIterator
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.api.routes import include_router
from src.utils.logger import setup_logging
from src.api.middlewares.request_logging import RequestLoggingMiddleware
from src.core.database import Base, engine


# Configurar logging UNA SOLA VEZ al inicio del módulo
setup_logging()
logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
    """Lifespan context manager for startup/shutdown events"""
    # startup logic
    logger.info("Starting app...")

    # Create database tables
    # async with engine.begin() as conn:
    #    await conn.run_sync(Base.metadata.create_all)
    # logger.info("Database tables created successfully")

    logger.info(f"Docs: http://{settings.HOST}:{settings.PORT}{settings.DOCS_URL}")

    yield  # App run here

    # shutdown logic
    await engine.dispose()
    logger.info("Application shutting down")


def create_app():
    """Creaet and configure fastapi application"""

    # app instance
    app = FastAPI(
        title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan
    )

    # cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # middleware
    app.add_middleware(RequestLoggingMiddleware)

    # include routes
    include_router(app)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG
    )
