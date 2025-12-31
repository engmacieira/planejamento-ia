from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class ETPDFD(Base):
    """
    Tabela Associativa: Vincula DFDs ao ETP.
    
    Regra de Negócio:
    1. Um ETP pode ter vários DFDs (1:N).
    2. Um DFD só pode pertencer a UM ETP.
       Isso é garantido pela 'UniqueConstraint' no campo 'dfd_id'.
    """
    __tablename__ = "etp_dfds"

    # TRAVA DE SEGURANÇA: Garante que o DFD não seja usado em dois ETPs diferentes.
    __table_args__ = (
        UniqueConstraint('dfd_id', name='uq_etp_dfds_dfd_unico'),
    )

    # Chave Primária Composta (Padrão SQLAlchemy)
    etp_id: Mapped[int] = mapped_column(ForeignKey("etps.id", ondelete="CASCADE"), primary_key=True)
    dfd_id: Mapped[int] = mapped_column(ForeignKey("dfds.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"<Link ETP {self.etp_id} - DFD {self.dfd_id}>"