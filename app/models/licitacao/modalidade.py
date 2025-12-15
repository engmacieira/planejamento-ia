from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Modalidade(Base):
    __tablename__ = "modalidade"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    sigla = Column(String(10))
    fundamentacao_legal = Column(String(255))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    numeros = relationship("app.models.licitacao.modalidade.NumeroModalidade", back_populates="modalidade")
    processos = relationship("app.models.licitacao.processo.ProcessoLicitatorio", back_populates="modalidade_ref")


class NumeroModalidade(Base):
    __tablename__ = "numeros_modalidade"

    id = Column(Integer, primary_key=True, index=True)
    id_modalidade = Column(Integer, ForeignKey("modalidade.id"), nullable=False)
    numero = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('id_modalidade', 'numero', 'ano', name='uk_modalidade_numero_ano'),
    )

    modalidade = relationship("app.models.licitacao.modalidade.Modalidade", back_populates="numeros")
    processos = relationship("app.models.licitacao.processo.ProcessoLicitatorio", back_populates="numero_modalidade_ref")
