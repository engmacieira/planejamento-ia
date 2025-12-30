from decimal import Decimal
from sqlalchemy import Integer, ForeignKey, String, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.gestao.aocs_model import Aocs
    from app.models.gestao.item_model import ItemContrato

class ItensAocs(Base):
    __tablename__ = "itens_aocs"
    
    __table_args__ = (
        CheckConstraint("quantidade_solicitada > 0", name="check_quantidade_solicitada_pos"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    id_aocs: Mapped[int] = mapped_column(ForeignKey("aocs.id", ondelete="CASCADE"))
    aocs: Mapped["Aocs"] = relationship("Aocs", lazy="selectin")
    
    id_item_contrato: Mapped[int] = mapped_column(ForeignKey("itens_contrato.id"))
    item_contrato: Mapped["ItemContrato"] = relationship("ItemContrato", lazy="selectin") # Assuming Item maps to itens_contrato
    
    quantidade_solicitada: Mapped[Decimal] = mapped_column(Numeric(15, 3))
    
    saldo_anterior_snapshot: Mapped[Decimal | None] = mapped_column(Numeric(15, 3), nullable=True)
    
    quantidade_entregue: Mapped[Decimal | None] = mapped_column(Numeric(15, 3), default=0)
    status_item: Mapped[str | None] = mapped_column(String(30), default='Aguardando Entrega')
