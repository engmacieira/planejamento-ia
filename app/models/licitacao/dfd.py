from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class DFD(Base):
    __tablename__ = "dfd"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    descricao_sucinta = Column(String(255), nullable=False)
    justificativa_necessidade = Column(Text)
    
    id_unidade_requisitante = Column(Integer, ForeignKey("unidades_requisitantes.id"), nullable=False)
    
    data_criacao = Column(Date, server_default=func.current_date())
    status = Column(String(50), default='Rascunho')

    __table_args__ = (
        UniqueConstraint('numero', 'ano', name='uk_dfd_numero_ano'),
    )

    unidade_requisitante = relationship("app.models.licitacao.unidade.UnidadeRequisitante", back_populates="dfds")
    processo = relationship("app.models.licitacao.processo.ProcessoLicitatorio", back_populates="dfd", uselist=False)
    itens = relationship("app.models.licitacao.item_dfd.ItemDFD", back_populates="dfd", cascade="all, delete-orphan")
