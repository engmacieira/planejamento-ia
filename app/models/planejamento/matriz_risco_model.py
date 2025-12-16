from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.etp_model import ETP
    from app.models.planejamento.item_risco_model import ItemRisco
    from app.models.planejamento.tr_model import TR

class MatrizRisco(Base):
    __tablename__ = "matrizes_risco"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    etp_id: Mapped[int | None] = mapped_column(ForeignKey("etps.id"), unique=True)
    etp: Mapped["ETP"] = relationship("ETP", back_populates="matriz")
    
    riscos: Mapped[list["ItemRisco"]] = relationship("ItemRisco", back_populates="matriz")
    tr: Mapped["TR"] = relationship("TR", back_populates="matriz", uselist=False)
