from datetime import date
from sqlalchemy import String, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel  

class Agente(DefaultModel, Base): 
    __tablename__ = "agentes_responsaveis"

    nome: Mapped[str] = mapped_column(String(255))
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    matricula: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cargo: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())
    data_atualizacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())