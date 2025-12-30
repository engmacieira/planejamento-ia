from datetime import date
from sqlalchemy import Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.modalidade_model import Modalidade

class NumeroModalidade(DefaultModel, Base): 
    __tablename__ = "numeros_modalidade"

    id_modalidade: Mapped[int] = mapped_column(ForeignKey("modalidades.id"))
    modalidade: Mapped["Modalidade"] = relationship("Modalidade", lazy="selectin")
    
    numero: Mapped[int] = mapped_column(Integer)
    ano: Mapped[int] = mapped_column(Integer)
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())