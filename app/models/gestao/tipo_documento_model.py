from datetime import date
from sqlalchemy import String, Text, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class TipoDocumento(Base):
    __tablename__ = "tipos_documento"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())
