from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.etp_model import ETP
    from app.models.gestao.dotacao_model import Dotacao

class ETPDotacao(Base):
    __tablename__ = "etp_dotacoes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    etp_id: Mapped[int | None] = mapped_column(ForeignKey("etps.id"))
    etp: Mapped["ETP"] = relationship("ETP", back_populates="dotacoes")
    
    dotacao_id: Mapped[int | None] = mapped_column(ForeignKey("dotacao.id"))
    dotacao: Mapped["Dotacao"] = relationship("Dotacao", lazy="selectin")
