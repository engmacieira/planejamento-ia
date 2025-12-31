from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.planejamento.etp_model import ETP
    from app.models.planejamento.item_risco_model import ItemRisco

class MatrizRisco(DefaultModel, Base):
    """
    Matriz de Gerenciamento de Riscos (Lei 14.133/21).
    Funciona como o 'cabeçalho' ou container para os riscos identificados no ETP.
    """
    __tablename__ = "matrizes_risco"

    # REGRA DE OURO: 1 ETP = 1 Matriz de Risco.
    # Garante que não sejam criadas múltiplas matrizes para o mesmo estudo.
    __table_args__ = (
        UniqueConstraint('etp_id', name='uq_matriz_risco_etp'),
    )

    # Vínculo com o ETP (Pai) - Cascade Delete
    # Se o ETP for excluído, a matriz inteira (e seus itens) vai junto.
    etp_id: Mapped[int] = mapped_column(ForeignKey("etps.id", ondelete="CASCADE"), nullable=False)

    # Relacionamentos
    
    # Back_populates deve bater com o nome 'matriz' lá no ETP
    etp: Mapped["ETP"] = relationship("ETP", back_populates="matriz")
    
    # Lista de Riscos (Itens)
    # Aqui ficam os riscos reais: "Fornecedor falir", "Entrega atrasar", etc.
    itens: Mapped[List["ItemRisco"]] = relationship(
        "ItemRisco", 
        back_populates="matriz", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<MatrizRisco (ETP {self.etp_id})>"