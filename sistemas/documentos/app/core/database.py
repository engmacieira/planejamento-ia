from sqlalchemy import create_engine, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Pega a URL do banco (se não tiver no env, usa sqlite local padrão)
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL", "sqlite:///./app.db")

# Cria o motor do banco
# check_same_thread=False é necessário apenas para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- NOSSO PADRÃO DE ARQUITETURA ---
# Criamos uma classe Mixin. Todas as nossas tabelas vão herdar dela.
# Isso garante que TODAS as tabelas tenham ID, datas e controle de deleção (Soft Delete).
class DefaultModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft Delete: Em vez de apagar, marcamos como True
    is_deleted = Column(Boolean, default=False)

# Função para pegar a conexão (Dependency Injection do FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()