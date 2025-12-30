from datetime import date
from sqlalchemy import String, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.gestao.contrato_model import Contrato

class Fornecedor(DefaultModel, Base): 
    __tablename__ = "fornecedores"
    
    razao_social: Mapped[str] = mapped_column(String(255))
    nome_fantasia: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cpf_cnpj: Mapped[str] = mapped_column(String(18), unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())

    contratos: Mapped[list["Contrato"]] = relationship("Contrato", back_populates="fornecedor")