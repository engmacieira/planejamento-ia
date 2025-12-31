from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Text, Computed, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.planejamento.matriz_risco_model import MatrizRisco

class ItemRisco(DefaultModel, Base):
    """
    Item individual da Matriz de Risco.
    Representa um evento incerto que pode impactar o objetivo da contratação.
    """
    __tablename__ = "itens_risco"

    # REGRAS DE INTEGRIDADE (Data Quality):
    # Garante que a escala Matriz 5x5 seja respeitada (1 a 5).
    __table_args__ = (
        CheckConstraint('probabilidade >= 1 AND probabilidade <= 5', name='chk_risco_probabilidade_1_5'),
        CheckConstraint('impacto >= 1 AND impacto <= 5', name='chk_risco_impacto_1_5'),
    )

    # Vínculo com a Matriz (Pai) - Cascade Delete
    matriz_id: Mapped[int] = mapped_column(ForeignKey("matrizes_risco.id", ondelete="CASCADE"), nullable=False)

    # Identificação do Risco
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, comment="Ex: Técnico, Externo, Administrativo")
    descricao: Mapped[str] = mapped_column(Text, nullable=False, comment="O que pode acontecer? (Evento)")
    
    # Cálculos (Escala 1 a 5)
    probabilidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="1 (Raro) a 5 (Quase Certo)")
    impacto: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="1 (Insignificante) a 5 (Catastrófico)")
    
    # Campo Calculado (Automático): Probabilidade * Impacto
    # O banco atualiza isso sozinho sempre que você mudar a prob ou impacto.
    nivel_risco: Mapped[int] = mapped_column(
        Integer, 
        Computed("probabilidade * impacto"), 
        nullable=False,
        comment="Calculado automaticamente: 1 a 25"
    )

    # Tratamento
    acao_preventiva: Mapped[str | None] = mapped_column(Text, nullable=True, comment="O que fazer para evitar que aconteça?")
    acao_contingencia: Mapped[str | None] = mapped_column(Text, nullable=True, comment="O que fazer se acontecer?")
    
    # Responsável pelo tratamento (Geralmente um papel, não um nome específico)
    responsavel: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Ex: Fiscal do Contrato, Fornecedor")

    # Relacionamentos
    matriz: Mapped["MatrizRisco"] = relationship("MatrizRisco", back_populates="itens")

    def __repr__(self):
        return f"<ItemRisco '{self.descricao[:20]}' (Nível: {self.nivel_risco})>"