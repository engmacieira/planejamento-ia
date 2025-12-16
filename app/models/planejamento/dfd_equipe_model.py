from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    from app.models.core.agente_model import Agente

class DFDEquipe(Base):
    __tablename__ = "dfd_equipe"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    dfd_id: Mapped[int | None] = mapped_column(ForeignKey("dfds.id"))
    dfd: Mapped["DFD"] = relationship("DFD", back_populates="equipe")
    
    agente_id: Mapped[int | None] = mapped_column(ForeignKey("agentes_responsaveis.id"))
    agente: Mapped["Agente"] = relationship("Agente", lazy="selectin")
    
    papel: Mapped[str | None] = mapped_column(String(50), nullable=True)
