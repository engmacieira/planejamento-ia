from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Text, Numeric, Computed, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    # Usamos TYPE_CHECKING para imports pesados/circulares
    from app.models.gestao.catalogo_item_model import CatalogoItem

class ItemDFD(DefaultModel, Base): 
    """
    Itens pertencentes a um Documento de Formalização de Demanda (DFD).
    Vincula a necessidade (DFD) ao Catálogo de Materiais/Serviços (Gestão).
    """
    __tablename__ = "itens_dfd"

    # Regra de Negócio: Não pode haver dois itens com o mesmo número no mesmo DFD.
    __table_args__ = (
        UniqueConstraint('dfd_id', 'numero_item', name='uq_item_dfd_numero'),
    )

    # Chaves Estrangeiras
    # ondelete="CASCADE" -> Se o DFD for apagado do banco, os itens morrem junto.
    dfd_id: Mapped[int] = mapped_column(ForeignKey("dfds.id", ondelete="CASCADE"), nullable=False)
    
    # Vínculo com o Catálogo (Gestão)
    # Importante: O sistema deve validar se o item está ativo no catálogo antes de inserir aqui.
    catalogo_item_id: Mapped[int] = mapped_column(ForeignKey("catalogo_itens.id"), nullable=False)
    
    # Dados do Item
    numero_item: Mapped[int] = mapped_column(Integer, nullable=False, comment="Sequencial: 1, 2, 3...")
    
    # Valores Monetários (Precisão Financeira)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(15, 3), nullable=False, default=1)
    valor_unitario_estimado: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Campo Calculado no Banco (Performance)
    # O banco calcula isso automaticamente, garantindo consistência.
    valor_total_estimado: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2), 
        Computed("quantidade * valor_unitario_estimado"), 
        nullable=True
    )
    
    complemento_descricao: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Detalhes específicos para esta compra")

    # Relacionamentos
    dfd: Mapped["DFD"] = relationship("DFD", back_populates="itens")
    catalogo_item: Mapped["CatalogoItem"] = relationship("CatalogoItem", lazy="selectin")

    def __repr__(self):
        return f"<ItemDFD {self.numero_item} (Total: {self.valor_total_estimado})>"