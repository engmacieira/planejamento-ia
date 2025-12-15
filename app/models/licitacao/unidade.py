from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class UnidadeRequisitante(Base):
    __tablename__ = "unidades_requisitantes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False)
    sigla = Column(String(20))
    codigo_administrativo = Column(String(20))
    
    id_unidade_pai = Column(Integer, ForeignKey("unidades_requisitantes.id"))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    unidade_pai = relationship("UnidadeRequisitante", remote_side=[id], backref="subunidades")
    dfds = relationship("app.models.licitacao.dfd.DFD", back_populates="unidade_requisitante")
