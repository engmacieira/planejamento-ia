from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.base_model import DefaultModel  

class Perfil(DefaultModel, Base): 
    __tablename__ = "perfis"
    
    nome: Mapped[str] = mapped_column(String(50), unique=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)