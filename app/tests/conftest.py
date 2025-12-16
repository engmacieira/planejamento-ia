import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.core.security import get_password_hash
# Import models to ensure they are registered with Base
import app.models 
from httpx import AsyncClient, ASGITransport
from app.core.security import create_access_token
from app.main import app 
from app.core.deps import get_db

# Use Async SQLite in-memory
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
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

@pytest.fixture(scope="function")
async def client(db_session):
    """
    Creates an AsyncClient for integration tests.
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def usuario_normal_token(db_session, sample_user):
    """
    Returns a valid access token for the sample_user.
    """
    access_token = create_access_token(data={"sub": str(sample_user.id)})
    return {"Authorization": f"Bearer {access_token}"}
