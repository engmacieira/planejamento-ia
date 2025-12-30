from decimal import Decimal
from sqlalchemy import Integer, ForeignKey, Text, Numeric, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel  

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    from app.models.gestao.catalogo_item_model import CatalogoItem

class ItemDFD(DefaultModel, Base): 
    __tablename__ = "itens_dfd"
    
    dfd_id: Mapped[int | None] = mapped_column(ForeignKey("dfds.id"))
    dfd: Mapped["DFD"] = relationship("DFD", back_populates="itens")
    
    catalogo_item_id: Mapped[int] = mapped_column(ForeignKey("catalogo_itens.id"))
    catalogo_item: Mapped["CatalogoItem"] = relationship("CatalogoItem", lazy="selectin")
    
    numero_item: Mapped[int] = mapped_column(Integer)
    
    quantidade: Mapped[Decimal] = mapped_column(Numeric(15, 3))
    valor_unitario_estimado: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    
    valor_total_estimado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), Computed("quantidade * valor_unitario_estimado"), nullable=True)
    
    complemento_descricao: Mapped[str | None] = mapped_column(Text, nullable=True)