from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.matriz_risco_model import MatrizRisco

class TR(Base):
    __tablename__ = "trs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    matriz_id: Mapped[int | None] = mapped_column(ForeignKey("matrizes_risco.id"), unique=True)
    matriz: Mapped["MatrizRisco"] = relationship("MatrizRisco", back_populates="tr")
    
    fundamentacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    # outros campos... placeholder
