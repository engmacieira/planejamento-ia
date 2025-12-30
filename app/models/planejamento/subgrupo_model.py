from sqlalchemy import String, ForeignKey, CHAR, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.grupo_model import Grupo

class Subgrupo(DefaultModel, Base): 
    __tablename__ = "subgrupos"
    
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.id"))
    
    codigo: Mapped[str] = mapped_column(CHAR(2))
    nome: Mapped[str] = mapped_column(String(150))
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    grupo: Mapped["Grupo"] = relationship("Grupo", backref="subgrupos", lazy="selectin")