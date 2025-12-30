from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.core.user_model import User
    from app.models.planejamento.dfd_model import DFD

class ProcessoDocumento(DefaultModel, Base):
    """
    Tabela 'Capa de Processo'.
    Wrapper ao redor do DFD para geração de documentos.
    """
    __tablename__ = "processos"

    dfd_id: Mapped[int] = mapped_column(ForeignKey("dfds.id"))
    dfd: Mapped["DFD"] = relationship("DFD", lazy="selectin")
    
    artigo: Mapped[str | None] = mapped_column(String, nullable=True)
    
    data1: Mapped[str | None] = mapped_column(String, nullable=True)
    data2: Mapped[str | None] = mapped_column(String, nullable=True)
    data3: Mapped[str | None] = mapped_column(String, nullable=True)
    data4: Mapped[str | None] = mapped_column(String, nullable=True)
    data5: Mapped[str | None] = mapped_column(String, nullable=True)
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id")) 
    
    owner: Mapped["User"] = relationship("User", back_populates="processos", lazy="selectin")

    @property
    def objeto(self) -> str | None:
        return self.dfd.descricao_sucinta if self.dfd else None