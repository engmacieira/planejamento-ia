from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Text, Numeric, Computed, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.planejamento.etp_model import ETP
    from app.models.gestao.catalogo_item_model import CatalogoItem

class ItemETP(DefaultModel, Base): 
    """
    Itens do Estudo Técnico Preliminar.
    Geralmente são importados/consolidados a partir dos itens dos DFDs vinculados.
    
    Aqui define-se o objeto da contratação de forma consolidada para estudo de mercado.
    """
    __tablename__ = "itens_etp"

    # Regra: Não pode haver item 1 e item 1 repetido no mesmo ETP.
    __table_args__ = (
        UniqueConstraint('etp_id', 'numero_item', name='uq_item_etp_numero'),
    )

    # --- Vínculos ---
    # Se o ETP for deletado, os itens somem (Cascade).
    etp_id: Mapped[int] = mapped_column(ForeignKey("etps.id", ondelete="CASCADE"), nullable=False)
    
    # O item deve existir no Catálogo de Materiais/Serviços (Gestão)
    catalogo_item_id: Mapped[int] = mapped_column(ForeignKey("catalogo_itens.id"), nullable=False)
    
    # --- Dados do Item ---
    numero_item: Mapped[int] = mapped_column(Integer, nullable=False, comment="Sequencial: 1, 2, 3...")
    
    # Quantidade Consolidada (Soma dos DFDs ou ajuste do planejador)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(15, 3), nullable=False, default=1)
    
    # Valor Unitário (Estimativa preliminar baseada no banco de preços ou média inicial)
    valor_unitario_estimado: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Campo Calculado Automaticamente (Performance e Integridade)
    valor_total_estimado: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2), 
        Computed("quantidade * valor_unitario_estimado"), 
        nullable=True
    )
    
    # Descrição Complementar (Pode ser refinada em relação ao DFD original)
    complemento_descricao: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Especificações técnicas refinadas durante o estudo")

    # --- Relacionamentos ---
    etp: Mapped["ETP"] = relationship("ETP", back_populates="itens")
    catalogo_item: Mapped["CatalogoItem"] = relationship("CatalogoItem", lazy="selectin")

    def __repr__(self):
        return f"<ItemETP {self.numero_item} (Total: {self.valor_total_estimado})>"