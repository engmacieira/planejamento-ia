from datetime import date
from decimal import Decimal
from sqlalchemy import String, Date, Numeric, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.gestao.aocs_model import Aocs

class Pedido(Base):
    __tablename__ = "pedido"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    id_item_contrato: Mapped[int] = mapped_column(Integer) # Legacy link
    id_aocs: Mapped[int] = mapped_column(ForeignKey("aocs.id"))
    aocs: Mapped["Aocs"] = relationship("Aocs", lazy="selectin")
    
    quantidade_pedida: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    data_pedido: Mapped[date] = mapped_column(Date)
    status_entrega: Mapped[str] = mapped_column(String)
    quantidade_entregue: Mapped[Decimal] = mapped_column(Numeric(10, 2))
