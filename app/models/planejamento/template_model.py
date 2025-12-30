from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.core.user_model import User
    from app.models.core.log_documento_model import GenerationLog

class Template(DefaultModel, Base): 
    __tablename__ = "templates"

    filename: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id")) 
    owner: Mapped["User"] = relationship("User", back_populates="templates", lazy="selectin")
    
    logs: Mapped[list["GenerationLog"]] = relationship("GenerationLog", back_populates="template")