from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel  

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.core.user_model import User
    from app.models.planejamento.template_model import Template

class GenerationLog(DefaultModel, Base): 
    __tablename__ = "generation_logs"
    
    generated_filename: Mapped[str] = mapped_column(String)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    user: Mapped["User"] = relationship("User", back_populates="logs")
    
    template_id: Mapped[int] = mapped_column(ForeignKey("templates.id"))
    template: Mapped["Template"] = relationship("Template", back_populates="logs")