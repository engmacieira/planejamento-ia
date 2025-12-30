from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    from app.models.gestao.dotacao_model import Dotacao

class DFDDotacao(Base):
    __tablename__ = "dfd_dotacoes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    dfd_id: Mapped[int | None] = mapped_column(ForeignKey("dfds.id"))
    dfd: Mapped["DFD"] = relationship("DFD", back_populates="dotacoes")
    
    dotacao_id: Mapped[int | None] = mapped_column(ForeignKey("dotacao.id")) # Referring to Gestao Dotacao table 'dotacao' (singular) as refined earlier
    dotacao: Mapped["Dotacao"] = relationship("Dotacao", lazy="selectin")
