from datetime import date
from typing import Any
from sqlalchemy import String, Integer, ForeignKey, Text, JSON, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    id_usuario: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    username_snapshot: Mapped[str | None] = mapped_column(String(80), nullable=True)
    
    data_acao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())
    ip_origem: Mapped[str | None] = mapped_column(String(45), nullable=True)
    
    tabela_afetada: Mapped[str] = mapped_column(String(100))
    id_registro_afetado: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tipo_acao: Mapped[str] = mapped_column(String(20))
    
    dados_antigos: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True) # JSONB in SQL maps to JSON in SA
    dados_novos: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    
    descricao_legivel: Mapped[str | None] = mapped_column(Text, nullable=True)
