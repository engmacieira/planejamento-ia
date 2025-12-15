from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Template(Base):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id")) # Linking to 'usuarios' table from gestao User
    owner: Mapped["User"] = relationship("User", back_populates="templates")
    
    logs: Mapped[list["GenerationLog"]] = relationship("GenerationLog", back_populates="template")
