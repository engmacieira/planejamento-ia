from datetime import date
from decimal import Decimal
from sqlalchemy import String, Date, Numeric, Integer, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.gestao.aocs_model import Aocs
    
class CiPagamento(DefaultModel, Base): 
    __tablename__ = "ci_pagamentos"
    
    id_aocs: Mapped[int] = mapped_column(ForeignKey("aocs.id"))
    aocs: Mapped["Aocs"] = relationship("Aocs", lazy="selectin")
    
    numero_ci: Mapped[str] = mapped_column(String(50), unique=True)
    data_ci: Mapped[date] = mapped_column(Date)
    
    id_solicitante: Mapped[int | None] = mapped_column(ForeignKey("agentes_responsaveis.id"), nullable=True)
    id_dotacao_pagamento: Mapped[int | None] = mapped_column(ForeignKey("dotacao.id"), nullable=True)
    
    numero_nota_fiscal: Mapped[str] = mapped_column(String(100))
    serie_nota_fiscal: Mapped[str | None] = mapped_column(String(50), nullable=True)
    data_nota_fiscal: Mapped[date] = mapped_column(Date)
    
    valor_nota_fiscal: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    
    codigo_acesso_nota: Mapped[str | None] = mapped_column(String(44), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())