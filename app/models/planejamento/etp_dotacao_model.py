from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel  

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.etp_model import ETP
    from app.models.gestao.dotacao_model import Dotacao

class ETPDotacao(DefaultModel, Base): 
    __tablename__ = "etp_dotacoes"
    
    etp_id: Mapped[int | None] = mapped_column(ForeignKey("etps.id"))
    etp: Mapped["ETP"] = relationship("ETP", back_populates="dotacoes")
    
    dotacao_id: Mapped[int | None] = mapped_column(ForeignKey("dotacao.id"))
    dotacao: Mapped["Dotacao"] = relationship("Dotacao", lazy="selectin")