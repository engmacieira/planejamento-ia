from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel 

if TYPE_CHECKING:
    from app.models.planejamento.etp_model import ETP
    from app.models.gestao.dotacao_model import Dotacao

class ETPDotacao(DefaultModel, Base): 
    """
    Dotações Orçamentárias vinculadas ao ETP.
    Representa a consolidação financeira dos DFDs.
    
    Lógica de Consolidação:
    Este registro agrupa os valores de dotações idênticas vindas de múltiplos DFDs.
    Ex: Se 3 DFDs usam a mesma ficha orçamentária, aqui teremos apenas 1 linha com a soma dos valores.
    """
    __tablename__ = "etp_dotacoes"

    # Regra: A mesma dotação só aparece uma vez dentro de um ETP (com o valor total somado).
    __table_args__ = (
        UniqueConstraint('etp_id', 'dotacao_id', name='uq_etp_dotacao_vinculo'),
    )

    # Vínculo com o Pai (ETP) - Cascade Delete
    etp_id: Mapped[int] = mapped_column(ForeignKey("etps.id", ondelete="CASCADE"), nullable=False)
    
    # Vínculo com a Gestão (Dotação)
    # Apontando corretamente para a tabela 'dotacoes' (plural)
    dotacao_id: Mapped[int] = mapped_column(ForeignKey("dotacoes.id"), nullable=False) 
    
    # Valor Consolidado
    # Este campo deve armazenar a SOMA dos 'valor_previsto' dos DFDDotacao correspondentes.
    valor_previsto: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0.00, comment="Soma do valor reservado nos DFDs")

    # Relacionamentos
    etp: Mapped["ETP"] = relationship("ETP", back_populates="dotacoes")
    dotacao: Mapped["Dotacao"] = relationship("Dotacao", lazy="selectin")

    def __repr__(self):
        return f"<ETPDotacao {self.id} - Dotação {self.dotacao_id} (R$ {self.valor_previsto})>"