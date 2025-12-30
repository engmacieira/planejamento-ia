from datetime import date
from sqlalchemy import String, Integer, ForeignKey, Text, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.core.unidade_model import Unidade
    from app.models.core.user_model import User
    from app.models.planejamento.dfd_equipe_model import DFDEquipe
    from app.models.planejamento.dfd_dotacao_model import DFDDotacao
    from app.models.planejamento.etp_model import ETP
    from app.models.planejamento.item_dfd_model import ItemDFD
    
class DFD(Base):
    __tablename__ = "dfds"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Campos de Identificação
    numero: Mapped[int] = mapped_column(Integer)
    ano: Mapped[int] = mapped_column(Integer)
    numero_protocolo_string: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    
    # Campos Descritivos
    descricao_sucinta: Mapped[str] = mapped_column(String(255))
    justificativa_necessidade: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_req: Mapped[date] = mapped_column(Date)
    
    # Relacionamentos (Foreign Keys)
    unidade_requisitante_id: Mapped[int] = mapped_column(ForeignKey("unidades_requisitantes.id"))
    
    # CORREÇÃO AQUI: "users.id" -> "usuarios.id"
    responsavel_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id")) 
    
    etp_id: Mapped[int | None] = mapped_column(ForeignKey("etps.id"), nullable=True)
    
    # Metadados
    data_criacao: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    status: Mapped[str | None] = mapped_column(String(50), default='Rascunho')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # --- Relacionamentos (ORM) ---
    unidade_requisitante: Mapped["Unidade"] = relationship("Unidade", lazy="selectin")
    responsavel: Mapped["User"] = relationship("User", lazy="selectin")
    
    itens: Mapped[list["ItemDFD"]] = relationship("ItemDFD", back_populates="dfd", cascade="all, delete-orphan")
    equipe: Mapped[list["DFDEquipe"]] = relationship("DFDEquipe", back_populates="dfd")
    dotacoes: Mapped[list["DFDDotacao"]] = relationship("DFDDotacao", back_populates="dfd")
    
    etp: Mapped["ETP"] = relationship("ETP", back_populates="dfds")