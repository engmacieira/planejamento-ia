from datetime import date
from sqlalchemy import String, Date, Integer, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base

# Importe os modelos relacionados para evitar erros de referência cruzada, se necessário
# from app.models.core.unidade_model import Unidade (Opcional, o SQLAlchemy resolve string, mas o import ajuda)

class Aocs(Base):
    __tablename__ = "aocs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    numero_aocs: Mapped[str] = mapped_column(String(100), unique=True)
    ano_aocs: Mapped[int] = mapped_column(Integer)
    
    numero_pedido_externo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    data_emissao: Mapped[date] = mapped_column(Date, default=func.current_date())
    
    # CORREÇÃO AQUI 👇 (unidades_requisitantes)
    id_unidade_requisitante: Mapped[int] = mapped_column(ForeignKey("unidades_requisitantes.id"))
    
    id_solicitante: Mapped[int | None] = mapped_column(ForeignKey("agentes_responsaveis.id"), nullable=True)
    id_agente_responsavel: Mapped[int | None] = mapped_column(ForeignKey("agentes_responsaveis.id"), nullable=True)
    
    # Relacionamentos
    # Dica: 'Agente' precisa estar importado ou disponível no registry
    solicitante: Mapped["Agente"] = relationship("Agente", foreign_keys=[id_solicitante], lazy="selectin")
    agente_responsavel: Mapped["Agente"] = relationship("Agente", foreign_keys=[id_agente_responsavel], lazy="selectin")
    
    id_local_entrega: Mapped[int | None] = mapped_column(ForeignKey("locais_entrega.id"), nullable=True)
    id_dotacao: Mapped[int | None] = mapped_column(ForeignKey("dotacao.id"), nullable=True)
    
    empenho: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    status: Mapped[str] = mapped_column(String(30), default='Emitida')
    justificativa: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())