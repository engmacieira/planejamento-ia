import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_async_db
from app.main import app  # Importe sua instância FastAPI
from typing import AsyncGenerator

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False 
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

@pytest.fixture(scope="session")
def event_loop():
    """Cria uma instância do loop de eventos para toda a sessão de testes."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Cria as tabelas, entrega uma sessão para o teste e depois limpa tudo.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session        
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client_db(db_session):
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_async_db] = override_get_db
    yield
    app.dependency_overrides.clear()