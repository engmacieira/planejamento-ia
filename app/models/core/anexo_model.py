from datetime import date
from sqlalchemy import String, ForeignKey, BigInteger, TIMESTAMP, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel  

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.gestao.contrato_model import Contrato
    from app.models.gestao.aocs_model import Aocs
    
class Anexo(DefaultModel, Base):
    __tablename__ = "anexos"
    
    __table_args__ = (
        CheckConstraint(
            "(id_contrato IS NOT NULL AND id_aocs IS NULL) OR (id_contrato IS NULL AND id_aocs IS NOT NULL)",
            name="check_origem_anexo"
        ),
    )
    
    nome_original: Mapped[str] = mapped_column(String(255))
    nome_seguro: Mapped[str] = mapped_column(String(255), unique=True)
    caminho_arquivo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tamanho_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    mimetype: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    id_tipo_documento: Mapped[int | None] = mapped_column(ForeignKey("tipos_documento.id"), nullable=True)
    
    id_contrato: Mapped[int | None] = mapped_column(ForeignKey("contratos.id", ondelete="CASCADE"), nullable=True)
    contrato: Mapped["Contrato"] = relationship("Contrato", lazy="selectin")

    id_aocs: Mapped[int | None] = mapped_column(ForeignKey("aocs.id", ondelete="CASCADE"), nullable=True)
    aocs: Mapped["Aocs"] = relationship("Aocs", lazy="selectin")
    
    data_upload: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())