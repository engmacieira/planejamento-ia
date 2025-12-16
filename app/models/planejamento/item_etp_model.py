from decimal import Decimal
from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.etp_model import ETP
    from app.models.gestao.catalogo_item_model import CatalogoItem

class ItemETP(Base):
    __tablename__ = "itens_etp"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    etp_id: Mapped[int | None] = mapped_column(ForeignKey("etps.id"))
    etp: Mapped["ETP"] = relationship("ETP", back_populates="itens")
    
    catalogo_item_id: Mapped[int | None] = mapped_column(ForeignKey("catalogo_itens.id"))
    catalogo_item: Mapped["CatalogoItem"] = relationship("CatalogoItem", lazy="selectin")
    
    quantidade_total: Mapped[Decimal | None] = mapped_column(Numeric(15, 3), nullable=True)
    valor_unitario_referencia: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    valor_total_estimado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
