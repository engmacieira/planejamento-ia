from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Numeric, UniqueConstraint, CheckConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    numero_contrato = Column(Integer, nullable=False)
    ano_contrato = Column(Integer, nullable=False)
    
    id_processo_licitatorio = Column(Integer, ForeignKey("processos_licitatorios.id"), nullable=False)
    id_numero_modalidade = Column(Integer, ForeignKey("numeros_modalidade.id"), nullable=False)
    id_fornecedor = Column(Integer, ForeignKey("fornecedores.id"), nullable=False)
    id_instrumento_contratual = Column(Integer, ForeignKey("instrumentos_contratuais.id"))
    
    data_assinatura = Column(Date, nullable=False)
    data_inicio_vigencia = Column(Date, nullable=False)
    data_fim_vigencia = Column(Date, nullable=False)
    
    valor_total = Column(Numeric(15, 2), default=0)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('numero_contrato', 'ano_contrato', name='uk_contrato_full'),
        CheckConstraint('data_fim_vigencia >= data_inicio_vigencia', name='check_vigencia'),
    )

    processo_licitatorio = relationship("app.models.licitacao.processo.ProcessoLicitatorio", back_populates="contratos")
    numero_modalidade = relationship("app.models.licitacao.modalidade.NumeroModalidade", backref="contratos")
    fornecedor = relationship("app.models.gestao.fornecedor.Fornecedor", back_populates="contratos")
    instrumento = relationship("app.models.gestao.instrumento.InstrumentoContratual", back_populates="contratos")
    itens = relationship("app.models.gestao.item_contrato.ItemContrato", back_populates="contrato", cascade="all, delete-orphan")
    anexos = relationship("app.models.documentos.Anexo", back_populates="contrato", cascade="all, delete-orphan")
