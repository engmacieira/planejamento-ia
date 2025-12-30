from datetime import date
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, Text, Numeric, Date, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    from app.models.planejamento.modalidade_model import Modalidade
    from app.models.planejamento.numero_modalidade_model import NumeroModalidade

class ProcessoLicitatorio(DefaultModel, Base): 
    __tablename__ = "processos_licitatorios"

    id_dfd: Mapped[int] = mapped_column(ForeignKey("dfds.id"))
    dfd: Mapped["DFD"] = relationship("DFD", lazy="selectin")
    
    numero_processo: Mapped[int] = mapped_column(Integer)
    ano_processo: Mapped[int] = mapped_column(Integer)
    
    id_modalidade: Mapped[int] = mapped_column(ForeignKey("modalidades.id"))
    modalidade: Mapped["Modalidade"] = relationship("Modalidade", lazy="selectin")
    
    id_numero_modalidade: Mapped[int | None] = mapped_column(ForeignKey("numeros_modalidade.id"), nullable=True)
    numero_modalidade_obj: Mapped["NumeroModalidade"] = relationship("NumeroModalidade", lazy="selectin")
    
    objeto: Mapped[str] = mapped_column(Text)
    
    valor_total_estimado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    data_abertura: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_homologacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    
    status: Mapped[str | None] = mapped_column(String(50), default='Em Andamento')
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())