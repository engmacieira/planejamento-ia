from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Perfil(Base):
    __tablename__ = "perfis"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)

    usuarios = relationship("Usuario", back_populates="perfil")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    id_perfil = Column(Integer, ForeignKey("perfis.id"), nullable=False)
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    nome_completo = Column(String(255), nullable=False)
    cpf = Column(String(11), unique=True, index=True)
    telefone = Column(String(20))
    
    ativo = Column(Boolean, default=True)
    ultimo_login = Column(DateTime(timezone=True))
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    perfil = relationship("Perfil", back_populates="usuarios")
