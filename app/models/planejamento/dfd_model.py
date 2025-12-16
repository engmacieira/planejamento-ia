from datetime import date
from sqlalchemy import String, Integer, ForeignKey, Text, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.core.unidade_model import Unidade
    from app.models.planejamento.dfd_equipe_model import DFDEquipe
    from app.models.planejamento.dfd_dotacao_model import DFDDotacao
    from app.models.planejamento.etp_model import ETP
    from app.models.planejamento.item_dfd_model import ItemDFD
    
class DFD(Base):
    __tablename__ = "dfds"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    numero: Mapped[int] = mapped_column(Integer)
    ano: Mapped[int] = mapped_column(Integer)
    numero_protocolo_string: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True) # Not in SQL, keeping as legacy artifact? Or remove? SQL doesn't have it. User said "merge info from SQL...". If SQL is source of truth, maybe keep optional.
    
    descricao_sucinta: Mapped[str] = mapped_column(String(255))
    justificativa_necessidade: Mapped[str | None] = mapped_column(Text, nullable=True) # Renamed from justificativa
    
    unidade_requisitante_id: Mapped[int] = mapped_column(ForeignKey("unidades_requisitantes.id"))
    unidade_requisitante: Mapped["Unidade"] = relationship("Unidade", lazy="selectin")

    etp_id: Mapped[int | None] = mapped_column(ForeignKey("etps.id"), nullable=True)
    
    # Responsavel not in dfd.sql? Checking SQL content again.
    # dfd.sql lines 1-19 do NOT show responsavel_id or etp_id.
    # Lines 1-19 show: id, numero, ano, descricao_sucinta, justificativa_necessidade, id_unidade_requisitante, data_criacao, status.
    # Meaning responsavel, etp, equipe, dotacoes are NOT in dfd.sql.
    # Strategy: Keep them as nullable (Code-First extensions) or if strict DB First, remove?
    # User said "mesclando informações previstas nos arquivos .sql eu ainda não estão nos models".
    # Implicitly: preserve code-only fields? Or if strict sync?
    # I will keep them but make sure SQL fields are correct.
    
    data_criacao: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    status: Mapped[str | None] = mapped_column(String(50), default='Rascunho')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    itens: Mapped[list["ItemDFD"]] = relationship("ItemDFD", back_populates="dfd", cascade="all, delete-orphan")
    equipe: Mapped[list["DFDEquipe"]] = relationship("DFDEquipe", back_populates="dfd")
    dotacoes: Mapped[list["DFDDotacao"]] = relationship("DFDDotacao", back_populates="dfd")
    
    etp: Mapped["ETP"] = relationship("ETP", back_populates="dfds")
