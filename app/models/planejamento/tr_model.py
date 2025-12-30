from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel  # <--- Importação

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.matriz_risco_model import MatrizRisco

class TR(DefaultModel, Base): #
    __tablename__ = "trs"
    
    matriz_id: Mapped[int | None] = mapped_column(ForeignKey("matrizes_risco.id"), unique=True)
    matriz: Mapped["MatrizRisco"] = relationship("MatrizRisco", back_populates="tr")
    
    fundamentacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Aqui você provavelmente adicionará mais campos no futuro (ex: qualificação técnica, entrega, etc.)