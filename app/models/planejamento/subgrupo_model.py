from sqlalchemy import String, Integer, ForeignKey, CHAR, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.grupo_model import Grupo

class Subgrupo(Base):
    __tablename__ = "subgrupos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.id"))
    codigo: Mapped[str] = mapped_column(CHAR(2))
    nome: Mapped[str] = mapped_column(String(150))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True) # Added from SQL
    
    grupo: Mapped["Grupo"] = relationship("Grupo", backref="subgrupos", lazy="selectin")
