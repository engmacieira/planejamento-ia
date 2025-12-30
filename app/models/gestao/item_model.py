from decimal import Decimal
from sqlalchemy import ForeignKey, String, Integer, Numeric, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.gestao.contrato_model import Contrato

class ItemContrato(DefaultModel, Base): # <--- Herança
    __tablename__ = "itens_contrato"

    id_contrato: Mapped[int] = mapped_column(ForeignKey("contratos.id", ondelete="CASCADE"))
    contrato: Mapped["Contrato"] = relationship("Contrato", backref="itens", lazy="selectin")
    
    id_item_dfd: Mapped[int] = mapped_column(ForeignKey("itens_dfd.id"))
    
    numero_item: Mapped[int] = mapped_column(Integer)
    
    marca: Mapped[str | None] = mapped_column(String(150), nullable=True)
    
    quantidade_contratada: Mapped[Decimal] = mapped_column(Numeric(15, 3))
    valor_unitario_final: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    
    valor_total_item: Mapped[Decimal] = mapped_column(Numeric(15, 2), Computed("quantidade_contratada * valor_unitario_final"))