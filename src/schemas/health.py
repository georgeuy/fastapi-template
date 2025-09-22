from datetime import datetime
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

    class Config:
        from_attributes = True
