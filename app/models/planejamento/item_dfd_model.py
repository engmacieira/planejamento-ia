from decimal import Decimal
from sqlalchemy import Integer, ForeignKey, Text, Numeric, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    from app.models.gestao.catalogo_item_model import CatalogoItem

class ItemDFD(Base):
    __tablename__ = "itens_dfd"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    dfd_id: Mapped[int | None] = mapped_column(ForeignKey("dfds.id"))
    dfd: Mapped["DFD"] = relationship("DFD", back_populates="itens")
    
    catalogo_item_id: Mapped[int] = mapped_column(ForeignKey("catalogo_itens.id"))
    catalogo_item: Mapped["CatalogoItem"] = relationship("CatalogoItem", lazy="selectin")
    
    numero_item: Mapped[int] = mapped_column(Integer)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(15, 3))
    valor_unitario_estimado: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    
    # Generated in DB
    valor_total_estimado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), Computed("quantidade * valor_unitario_estimado"), nullable=True)
    
    complemento_descricao: Mapped[str | None] = mapped_column(Text, nullable=True) # Not in SQL but useful? items_dfd.sql has no complemento_descricao.
    # check lines 1-22 of itens_dfd.sql again.
    # it has: id, id_dfd, id_catalogo_item, numero_item, quantidade, valor_unitario_estimado, valor_total_estimado.
    # No complemento_descricao. I will keep it as nullable (Code-first addition) if needed, or comment it out if strict?
    # User said "mesclando". I'll keep it.
