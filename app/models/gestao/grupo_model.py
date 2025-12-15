from sqlalchemy import String, Integer, ForeignKey, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Grupo(Base):
    __tablename__ = "grupos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    codigo: Mapped[str] = mapped_column(CHAR(2))
    nome: Mapped[str] = mapped_column(String(150))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True) # Added from SQL
    
    categoria: Mapped["Categoria"] = relationship("Categoria", backref="grupos", lazy="selectin")
