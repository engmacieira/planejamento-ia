import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport

from app.core.database import Base, get_async_db
from app.main import app

# URL do banco em memória (Rápido e isolado)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """
    Gerencia o loop de eventos para o escopo da sessão.
    Necessário para evitar erro de 'ScopeMismatch' em testes async.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db_engine():
    """
    Cria o motor do banco de dados para a sessão de testes.
    CRÍTICO: O 'await engine.dispose()' no final é o que libera o terminal.
    """
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,  # Não mantém conexões em cache (Vital para testes)
        echo=False
    )

    yield engine

    # --- O PULO DO GATO ---
    # Fecha todas as conexões abertas. Sem isso, o terminal trava.
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Entrega uma sessão limpa para cada teste (Isolamento total).
    """
    # 1. Cria as tabelas no banco em memória
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Cria a fábrica de sessões vinculada ao engine atual
    TestingSessionLocal = sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )

    # 3. Entrega a sessão para o teste usar
    async with TestingSessionLocal() as session:
        yield session
        # Garante rollback se o teste falhar
        await session.rollback()

    # 4. Limpa tudo (Drop) para o próximo teste não ver dados antigos
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client_db(db_session):
    """
    Cliente HTTP para testes de integração (Rotas).
    Substitui a dependência real do banco pela sessão de teste.
    """
    async def override_get_async_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_async_db
    
    # Configuração correta para versões recentes do httpx/FastAPI
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()