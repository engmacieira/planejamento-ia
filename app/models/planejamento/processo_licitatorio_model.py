from datetime import date
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, Text, Numeric, Date, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class ProcessoLicitatorio(Base):
    __tablename__ = "processos_licitatorios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Vínculo com a Origem
    id_dfd: Mapped[int] = mapped_column(ForeignKey("dfds.id")) # Assuming dfd table exists or will be created
    
    numero_processo: Mapped[int] = mapped_column(Integer)
    ano_processo: Mapped[int] = mapped_column(Integer)
    
    id_modalidade: Mapped[int] = mapped_column(ForeignKey("modalidades.id"))
    id_numero_modalidade: Mapped[int | None] = mapped_column(ForeignKey("numeros_modalidade.id"), nullable=True)
    
    objeto: Mapped[str] = mapped_column(Text)
    
    valor_total_estimado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    data_abertura: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_homologacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    
    status: Mapped[str | None] = mapped_column(String(50), default='Em Andamento')
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())

    # Constraints defined in SQL (uk_processo_adm, uk_processo_dfd) are managed by naming convention or explicit UniqueConstraint in __table_args__ if needed by logic, but for now mapped_column suffices for structure.
