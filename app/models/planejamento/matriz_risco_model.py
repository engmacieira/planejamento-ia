from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.etp_model import ETP
    from app.models.planejamento.item_risco_model import ItemRisco
    from app.models.planejamento.tr_model import TR

class MatrizRisco(DefaultModel, Base): 
    __tablename__ = "matrizes_risco"

    etp_id: Mapped[int | None] = mapped_column(ForeignKey("etps.id"), unique=True)
    etp: Mapped["ETP"] = relationship("ETP", back_populates="matriz")
    
    riscos: Mapped[list["ItemRisco"]] = relationship("ItemRisco", back_populates="matriz", cascade="all, delete-orphan")
    
    tr: Mapped["TR"] = relationship("TR", back_populates="matriz", uselist=False)