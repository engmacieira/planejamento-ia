from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Numeric, UniqueConstraint, CheckConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class AgenteResponsavel(Base):
    __tablename__ = "agentes_responsaveis"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    email = Column(String(255))
    telefone = Column(String(20))
    cargo = Column(String(100))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now())

class LocalEntrega(Base):
    __tablename__ = "locais_entrega"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), unique=True, nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100))
    bairro = Column(String(100), nullable=False)
    cep = Column(String(10))
    telefone_contato = Column(String(20))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

class Dotacao(Base):
    __tablename__ = "dotacao"

    id = Column(Integer, primary_key=True, index=True)
    exercicio = Column(Integer, nullable=False)
    codigo_dotacao = Column(String(100), nullable=False)
    numero_ficha = Column(Integer)
    descricao = Column(Text)
    saldo_inicial = Column(Numeric(15, 2))
    ativo = Column(Boolean, default=True)
    
    __table_args__ = (
        UniqueConstraint('exercicio', 'codigo_dotacao', name='uk_dotacao_exercicio_codigo'),
    )
