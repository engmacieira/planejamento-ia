import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.core.security import get_password_hash
# Import models to ensure they are registered with Base
import app.models 

# Use Async SQLite in-memory
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

TestingSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Pytest-asyncio: Override event_loop based on scope if needed, 
# but usually asyncio_mode = auto in pytest.ini is enough.

@pytest.fixture(scope="function")
async def db_session():
    """
    Creates a fresh async database session for each test function.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
        # No need to explicitly drop if using :memory: per check, but safe to drop.
        # But for async sqlite :memory:, usually shared engine holds it.
        # With create_async_engine and :memory:, data persists while engine is alive?
        # Actually in-memory sqlite is per connection if url is default, but shared if cache=shared.
        # Let's drop all at end of session.
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def sample_user(db_session):
    """
    Creates a sample user in the database.
    """
    from app.models.core.user_model import User
    
    password_hash = get_password_hash("123456")
    user = User(
        username="testuser",
        email="test@example.com",
        nome_completo="Test User",
        password_hash=password_hash,
        cpf="00011122233"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
async def sample_unidade(db_session):
    """
    Creates a sample unit in the database.
    """
    from app.models.core.unidade_model import Unidade
    
    unidade = Unidade(
        nome="Secretaria Teste",
        sigla="ST",
        codigo_administrativo="001"
    )
    db_session.add(unidade)
    await db_session.commit()
    await db_session.refresh(unidade)
    return unidade
