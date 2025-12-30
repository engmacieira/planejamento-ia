from datetime import date
from sqlalchemy import String, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class Local(Base):
    __tablename__ = "locais_entrega"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    nome: Mapped[str] = mapped_column(String(200), unique=True)
    
    logradouro: Mapped[str] = mapped_column(String(255))
    numero: Mapped[str] = mapped_column(String(20))
    complemento: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bairro: Mapped[str] = mapped_column(String(100))
    cep: Mapped[str | None] = mapped_column(String(10), nullable=True)
    
    telefone_contato: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())
