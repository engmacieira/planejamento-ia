from datetime import date
from sqlalchemy import String, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel  

class Categoria(DefaultModel, Base): 
    __tablename__ = "categorias"
    
    nome: Mapped[str] = mapped_column(String(150), unique=True)
    
    codigo_taxonomia: Mapped[str] = mapped_column(String(2), unique=True)
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())