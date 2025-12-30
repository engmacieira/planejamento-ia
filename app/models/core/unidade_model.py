from datetime import date
from sqlalchemy import String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel  

class Unidade(DefaultModel, Base): 
    __tablename__ = "unidades_requisitantes"
    
    nome: Mapped[str] = mapped_column(String(255), unique=True)
    sigla: Mapped[str | None] = mapped_column(String(20), nullable=True)
    codigo_administrativo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    id_unidade_pai: Mapped[int | None] = mapped_column(ForeignKey("unidades_requisitantes.id"), nullable=True)
    
    unidade_pai: Mapped["Unidade"] = relationship("Unidade", remote_side="Unidade.id", lazy="selectin")
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())