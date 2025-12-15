from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Numeric, UniqueConstraint, CheckConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255))
    cpf_cnpj = Column(String(18), unique=True, nullable=False)
    email = Column(String(255))
    telefone = Column(String(20))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    contratos = relationship("app.models.gestao.contrato.Contrato", back_populates="fornecedor")
