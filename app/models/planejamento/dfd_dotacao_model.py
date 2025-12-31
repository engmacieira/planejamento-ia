from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel 

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    from app.models.gestao.dotacao_model import Dotacao

class DFDDotacao(DefaultModel, Base): 
    """
    Tabela associativa entre DFD e Dotação Orçamentária.
    Define de onde sairá o dinheiro para este planejamento.
    """
    __tablename__ = "dfd_dotacoes"

    # Regra: Não pode vincular a mesma dotação duas vezes ao mesmo DFD.
    __table_args__ = (
        UniqueConstraint('dfd_id', 'dotacao_id', name='uq_dfd_dotacao_vinculo'),
    )

    # Vínculo com o Pai (DFD)
    # ondelete="CASCADE": Se o DFD morrer, esse vínculo morre.
    dfd_id: Mapped[int] = mapped_column(ForeignKey("dfds.id", ondelete="CASCADE"), nullable=False)
    
    # Vínculo com a Gestão (Dotação)
    # ATENÇÃO: Verifique se o __tablename__ lá no 'dotacao_model.py' é 'dotacoes' ou 'dotacao'.
    # Estou padronizando para 'dotacoes'. Na refatoração da Gestão, garantiremos isso.
    dotacao_id: Mapped[int] = mapped_column(ForeignKey("dotacoes.id"), nullable=False) 
    
    # Regra de Negócio: Quanto vamos usar dessa dotação?
    valor_previsto: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True, comment="Valor reservado desta dotação para este DFD")

    # Relacionamentos
    dfd: Mapped["DFD"] = relationship("DFD", back_populates="dotacoes")
    dotacao: Mapped["Dotacao"] = relationship("Dotacao", lazy="selectin")

    def __repr__(self):
        return f"<DFDDotacao {self.id} (R$ {self.valor_previsto})>"