import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool # <--- 1. IMPORTAR ISTO
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.main import app

# Importamos os models para garantir o registro no Base
from app.models.user_model import User
from app.models.template_model import Template
from app.models.log_model import GenerationLog

# Configuração do Banco em Memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool # <--- 2. ADICIONAR ISTO
)

# Evento para ativar Foreign Keys no SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Cria as tabelas
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Destroi as tabelas para o próximo teste vir limpo
        Base.metadata.drop_all(bind=engine)
        
@pytest.fixture(scope="function")
def client(db_session):
    """
    Cria um TestClient que substitui a conexão real do banco (get_db)
    pela nossa conexão de teste (db_session).
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass 

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()