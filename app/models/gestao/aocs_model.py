from datetime import date
from sqlalchemy import String, Integer, ForeignKey, Text, Date, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.core.agente_model import Agente
    from app.models.gestao.itens_aocs_model import ItensAocs

class Aocs(DefaultModel, Base):
    __tablename__ = "aocs"
    
    numero_aocs: Mapped[str] = mapped_column(String(100), unique=True)
    ano_aocs: Mapped[int] = mapped_column(Integer)
    
    numero_pedido_externo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    data_emissao: Mapped[date] = mapped_column(Date, default=func.current_date())
    
    id_unidade_requisitante: Mapped[int] = mapped_column(ForeignKey("unidades_requisitantes.id"))
    
    id_solicitante: Mapped[int | None] = mapped_column(ForeignKey("agentes_responsaveis.id"), nullable=True)
    id_agente_responsavel: Mapped[int | None] = mapped_column(ForeignKey("agentes_responsaveis.id"), nullable=True)
    
    solicitante: Mapped["Agente"] = relationship("Agente", foreign_keys=[id_solicitante], lazy="selectin")
    agente_responsavel: Mapped["Agente"] = relationship("Agente", foreign_keys=[id_agente_responsavel], lazy="selectin")
    
    id_local_entrega: Mapped[int | None] = mapped_column(ForeignKey("locais_entrega.id"), nullable=True)
    id_dotacao: Mapped[int | None] = mapped_column(ForeignKey("dotacao.id"), nullable=True)
    
    empenho: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    status: Mapped[str] = mapped_column(String(30), default='Emitida')
    justificativa: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    itens: Mapped[list["ItensAocs"]] = relationship("ItensAocs", back_populates="aocs", cascade="all, delete-orphan")
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())