from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.matriz_risco_model import MatrizRisco

class ItemRisco(Base):
    __tablename__ = "itens_risco"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    matriz_id: Mapped[int | None] = mapped_column(ForeignKey("matrizes_risco.id"))
    matriz: Mapped["MatrizRisco"] = relationship("MatrizRisco", back_populates="riscos")
    
    descricao_risco: Mapped[str | None] = mapped_column(Text, nullable=True)
    probabilidade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    impacto: Mapped[str | None] = mapped_column(String(50), nullable=True)
    medida_preventiva: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsavel: Mapped[str | None] = mapped_column(Text, nullable=True)
