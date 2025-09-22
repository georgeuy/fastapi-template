from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.core.config import settings


# database engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Session factory
AsycSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

# Base model
Base = declarative_base()


async def get_db():
    """Dependency for getting database session"""
    async with AsycSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
