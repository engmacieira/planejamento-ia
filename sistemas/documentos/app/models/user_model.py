from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.database import Base, DefaultModel

class User(Base, DefaultModel):
    # 1. Nome da tabela no banco (sempre no plural por convenção)
    __tablename__ = "users"

    # 2. Colunas Específicas
    # (Lembre-se: ID, created_at, updated_at e is_deleted já vêm do DefaultModel)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False) # Nunca salvamos senha pura!

    # 3. Relacionamentos (Ganchos para o futuro)
    # "Template" é o nome da classe que vamos criar. 
    # back_populates cria o caminho de volta.
    templates = relationship("Template", back_populates="owner")
    logs = relationship("GenerationLog", back_populates="user")
    processos = relationship("Processo", back_populates="owner")