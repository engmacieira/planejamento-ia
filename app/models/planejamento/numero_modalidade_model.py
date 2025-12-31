from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel 

if TYPE_CHECKING:
    from app.models.planejamento.modalidade_model import Modalidade

class NumeroModalidade(DefaultModel, Base): 
    """
    Controle de Numeração de Modalidades.
    Registra os números utilizados (Ex: Pregão 01/2025).
    """
    __tablename__ = "numeros_modalidades"

    # Regra: Para uma modalidade e ano, o número é único.
    __table_args__ = (
        UniqueConstraint('modalidade_id', 'ano', 'numero', name='uq_numero_modalidade_ano'),
    )

    # Identificação
    # Padronizado para 'modalidade_id' (FK)
    modalidade_id: Mapped[int] = mapped_column(ForeignKey("modalidades.id"), nullable=False)
    
    # A Numeração Reservada
    numero: Mapped[int] = mapped_column(Integer, nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relacionamentos
    modalidade: Mapped["Modalidade"] = relationship("Modalidade", lazy="selectin")

    def __repr__(self):
        return f"<NumeroModalidade {self.numero}/{self.ano} (Mod: {self.modalidade_id})>"