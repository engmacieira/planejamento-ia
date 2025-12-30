from sqlalchemy import String, ForeignKey, CHAR, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.categoria_model import Categoria

class Grupo(DefaultModel, Base): 
    __tablename__ = "grupos"
    
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    
    codigo: Mapped[str] = mapped_column(CHAR(2))
    nome: Mapped[str] = mapped_column(String(150))
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    categoria: Mapped["Categoria"] = relationship("Categoria", backref="grupos", lazy="selectin")