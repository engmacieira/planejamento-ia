from decimal import Decimal
from sqlalchemy import ForeignKey, String, Integer, Boolean, Numeric, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.gestao.contrato_model import Contrato

class ItemContrato(Base): # Renamed from Item for clarity/consistency
    __tablename__ = "itens_contrato"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Vínculo com o Contrato
    id_contrato: Mapped[int] = mapped_column(ForeignKey("contratos.id", ondelete="CASCADE"))
    contrato: Mapped["Contrato"] = relationship("Contrato", backref="itens", lazy="selectin")
    
    # Vínculo com a Origem da Demanda
    # Aponta para itens_dfd.id (tabela 'itens_dfd')
    id_item_dfd: Mapped[int] = mapped_column(ForeignKey("itens_dfd.id"))
    
    numero_item: Mapped[int] = mapped_column(Integer)
    
    marca: Mapped[str | None] = mapped_column(String(150), nullable=True)
    
    quantidade_contratada: Mapped[Decimal] = mapped_column(Numeric(15, 3))
    valor_unitario_final: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    
    # Coluna gerada
    valor_total_item: Mapped[Decimal] = mapped_column(Numeric(15, 2), Computed("quantidade_contratada * valor_unitario_final"))
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    # placeholder para futuras implementações de métodos de domínio
