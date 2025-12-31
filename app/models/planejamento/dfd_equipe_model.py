from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    from app.models.core.agente_model import Agente

class DFDEquipe(DefaultModel, Base):
    """
    Define quem faz parte da Equipe de Planejamento deste DFD.
    Geralmente composto por Integrante Técnico, Integrante Administrativo, Presidente, etc.
    """
    __tablename__ = "dfd_equipes"

    # Regra: Um agente só pode aparecer uma vez na equipe do mesmo DFD.
    __table_args__ = (
        UniqueConstraint('dfd_id', 'agente_id', name='uq_dfd_equipe_agente'),
    )

    # Vínculo com o Pai (DFD)
    dfd_id: Mapped[int] = mapped_column(ForeignKey("dfds.id", ondelete="CASCADE"), nullable=False)
    
    # Vínculo com o Core (Agente)
    # Lembre-se: Refatoramos a tabela de Agente para 'agentes_responsaveis'
    agente_id: Mapped[int] = mapped_column(ForeignKey("agentes_responsaveis.id"), nullable=False)
    
    # Papel na Equipe
    papel: Mapped[str] = mapped_column(String(50), nullable=False, default="Integrante", comment="Ex: Presidente, Fiscal, Técnico")

    # Relacionamentos
    dfd: Mapped["DFD"] = relationship("DFD", back_populates="equipe")
    agente: Mapped["Agente"] = relationship("Agente", lazy="selectin")

    def __repr__(self):
        return f"<DFDEquipe {self.papel} - Agente {self.agente_id}>"