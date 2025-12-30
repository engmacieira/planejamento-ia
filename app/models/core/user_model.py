from datetime import date
from sqlalchemy import String, Integer, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.template_model import Template
    from app.models.core.log_documento_model import GenerationLog
    from app.models.planejamento.processo_documento_model import ProcessoDocumento

class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    id_perfil: Mapped[int | None] = mapped_column(ForeignKey("perfis.id"), nullable=True) # Assuming perfis table exists
    
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    
    nome_completo: Mapped[str] = mapped_column(String(255))
    cpf: Mapped[str | None] = mapped_column(String(11), unique=True, nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    ultimo_login: Mapped[date | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())

    # Relationships from Documentos System
    templates: Mapped[list["Template"]] = relationship("Template", back_populates="owner")
    logs: Mapped[list["GenerationLog"]] = relationship("GenerationLog", back_populates="user")
    processos: Mapped[list["ProcessoDocumento"]] = relationship("ProcessoDocumento", back_populates="owner")

    def verificar_senha(self, senha_pura: str) -> bool:
        return check_password_hash(self.password_hash, senha_pura)

    @property
    def is_active(self) -> bool:
        return self.ativo
