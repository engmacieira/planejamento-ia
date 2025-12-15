from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Numeric, UniqueConstraint, CheckConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.gestao.auxiliares import AgenteResponsavel, LocalEntrega, Dotacao


class AOCS(Base):
    __tablename__ = "aocs"

    id = Column(Integer, primary_key=True, index=True)
    numero_aocs = Column(String(100), unique=True, nullable=False)
    ano_aocs = Column(Integer, nullable=False)
    numero_pedido_externo = Column(String(50))
    data_emissao = Column(Date, nullable=False, server_default=func.current_date())
    
    id_unidade_requisitante = Column(Integer, ForeignKey("unidades_requisitantes.id"), nullable=False)
    id_solicitante = Column(Integer, ForeignKey("agentes_responsaveis.id"))
    id_agente_responsavel = Column(Integer, ForeignKey("agentes_responsaveis.id"))
    
    id_local_entrega = Column(Integer, ForeignKey("locais_entrega.id"))
    id_dotacao = Column(Integer, ForeignKey("dotacao.id"))
    empenho = Column(String(50))
    
    status = Column(String(30), default='Emitida')
    justificativa = Column(Text)
    
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    unidade_requisitante = relationship("app.models.licitacao.unidade.UnidadeRequisitante")
    solicitante = relationship("AgenteResponsavel", foreign_keys=[id_solicitante]) # Mantendo no mesmo arquivo ou importando Agente? Vou deixar Agente aqui por simplicidade ou criar arquivo
    agente_responsavel = relationship("AgenteResponsavel", foreign_keys=[id_agente_responsavel])
    local_entrega = relationship("LocalEntrega")
    dotacao = relationship("Dotacao")
    anexos = relationship("app.models.documentos.Anexo", back_populates="aocs", cascade="all, delete-orphan")

# Agente, Local, Dotacao podem ficar neste mesmo arquivo 'auxiliares.py' ou separados.
# Vou separar para manter o padrão "granular".
