from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.core.user_model import User

class Unidade(DefaultModel, Base):
    """
    Representa as Unidades Requisitantes.
    Agora suporta relação N:N com Usuários.
    """
    __tablename__ = "unidades"

    nome: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    sigla: Mapped[str] = mapped_column(String(20), nullable=True)
    codigo_interno: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relacionamento Reverso Múltiplo
    users: Mapped[list["User"]] = relationship(
        "User", 
        secondary="usuarios_unidades", 
        back_populates="unidades"
    )

    def __repr__(self):
        return f"<Unidade {self.nome}>"