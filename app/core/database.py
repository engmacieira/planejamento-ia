from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import settings

# Sync Engine (Legacy/Compatibility)
engine = create_engine(settings.DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async Engine (New Standard)
# Ensure URL uses asyncpg driver
async_db_url = settings.DB_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(async_db_url, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

def get_db():
    """
    Sync Dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """
    Async Dependency.
    """
    async with AsyncSessionLocal() as session:
        yield session
