from fastapi import APIRouter
from src.api.controllers.health import HealthController
from src.schemas.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the API is running properly",
)
async def health_check():
    return await HealthController.health_check()
