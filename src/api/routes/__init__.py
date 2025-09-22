from fastapi import FastAPI
from .health import router as health_router


PREFIX = "/api/v1"


def include_router(app: FastAPI):
    app.include_router(health_router, prefix=PREFIX)
