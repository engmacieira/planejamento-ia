from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.planejamento.etp_model import ETP
    from app.models.core.agente_model import Agente

class ETPEquipe(DefaultModel, Base):
    """
    Equipe de Planejamento do ETP.
    Consolidada a partir das equipes dos DFDs vinculados.
    """
    __tablename__ = "etp_equipes"

    # REGRA DE OURO (Consolidação):
    # O mesmo agente pode aparecer mais de uma vez APENAS se tiver papéis diferentes.
    # Ex: João (Técnico) e João (Fiscal) -> Permitido.
    # Ex: João (Técnico) e João (Técnico) -> Bloqueado (Unicidade).
    __table_args__ = (
        UniqueConstraint('etp_id', 'agente_id', 'papel', name='uq_etp_equipe_agente_papel'),
    )

    # Vínculo com o Pai (ETP) - Cascade Delete
    etp_id: Mapped[int] = mapped_column(ForeignKey("etps.id", ondelete="CASCADE"), nullable=False)
    
    # Vínculo com o Core (Agente)
    # Lembre-se: A tabela no banco se chama 'agentes_responsaveis' (definido no core)
    agente_id: Mapped[int] = mapped_column(ForeignKey("agentes_responsaveis.id"), nullable=False)
    
    # Função Desempenhada
    papel: Mapped[str] = mapped_column(String(50), nullable=False, default="Integrante", comment="Ex: Presidente, Técnico, Fiscal")

    # Relacionamentos
    etp: Mapped["ETP"] = relationship("ETP", back_populates="equipe")
    agente: Mapped["Agente"] = relationship("Agente", lazy="selectin")

    def __repr__(self):
        return f"<ETPEquipe {self.papel} - Agente {self.agente_id}>"