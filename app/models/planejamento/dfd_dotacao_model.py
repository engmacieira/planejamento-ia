from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    from app.models.gestao.dotacao_model import Dotacao

class DFDDotacao(DefaultModel, Base): 
    __tablename__ = "dfd_dotacoes"

    dfd_id: Mapped[int | None] = mapped_column(ForeignKey("dfds.id"))
    dfd: Mapped["DFD"] = relationship("DFD", back_populates="dotacoes")
    
    dotacao_id: Mapped[int | None] = mapped_column(ForeignKey("dotacao.id")) 
    dotacao: Mapped["Dotacao"] = relationship("Dotacao", lazy="selectin")