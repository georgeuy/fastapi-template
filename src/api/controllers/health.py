from datetime import datetime, timezone
from src.core.config import settings
from src.schemas.health import HealthResponse


class HealthController:
    """Controller for health check endpoints"""

    @staticmethod
    async def health_check() -> HealthResponse:
        """Perform health check"""
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(timezone.utc),
            version=settings.VERSION,
        )
