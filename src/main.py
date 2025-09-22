import logging
from fastapi import FastAPI
from src.core.config import settings
from src.api.routes import include_router
from src.utils.logger import setup_logging
from src.api.middlewares.request_logging import RequestLoggingMiddleware

logger = logging.getLogger(__name__)


# set logger utility
setup_logging()

# app instance
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
logger.info("App started ...")

# cors

# middleware
app.add_middleware(RequestLoggingMiddleware)

# routes
include_router(app)
