from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class ProcessoLicitatorio(Base):
    __tablename__ = "processos_licitatorios"

    id = Column(Integer, primary_key=True, index=True)
    id_dfd = Column(Integer, ForeignKey("dfd.id"), unique=True, nullable=False)
    
    numero_processo = Column(Integer, nullable=False)
    ano_processo = Column(Integer, nullable=False)
    
    id_modalidade = Column(Integer, ForeignKey("modalidade.id"), nullable=False)
    id_numero_modalidade = Column(Integer, ForeignKey("numeros_modalidade.id"))
    
    objeto = Column(Text, nullable=False)
    valor_total_estimado = Column(Numeric(15, 2))
    
    data_abertura = Column(Date)
    data_homologacao = Column(Date)
    status = Column(String(50), default='Em Andamento')
    
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('numero_processo', 'ano_processo', name='uk_processo_adm'),
    )

    dfd = relationship("app.models.licitacao.dfd.DFD", back_populates="processo")
    modalidade_ref = relationship("app.models.licitacao.modalidade.Modalidade", back_populates="processos")
    numero_modalidade_ref = relationship("app.models.licitacao.modalidade.NumeroModalidade", back_populates="processos")
    contratos = relationship("app.models.gestao.contrato.Contrato", back_populates="processo_licitatorio")
