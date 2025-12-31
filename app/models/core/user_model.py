from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.core.database import Base
from app.core.base_model import DefaultModel

# Precisamos importar o modelo de associação para o SQLAlchemy saber que ele existe
# Mas usamos import condicional ou string para evitar erro circular
if TYPE_CHECKING:
    from app.models.core.unidade_model import Unidade
    from app.models.core.perfil_model import Perfil
    from app.models.core.log_documento_model import LogDocumento

class User(DefaultModel, Base):
    """
    Representa o Usuário do Sistema (Login).
    """
    __tablename__ = "usuarios"

    # Credenciais
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_completo: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Controle de Acesso (Diferença Importante)
    # is_active = False -> Usuário bloqueado (ex: férias, licença), mas histórico visível.
    # is_deleted = True -> Usuário excluído (ex: erro de cadastro), sumiu do sistema.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relacionamentos
    
    # 1. Perfil (Nível de Acesso - Admin, Gestor...)
    perfil_id: Mapped[int | None] = mapped_column(ForeignKey("perfis.id"), nullable=True)
    perfil: Mapped["Perfil"] = relationship("Perfil", back_populates="users", lazy="selectin")

    # 2. Unidades (Secretarias onde trabalha - Agora Múltiplas!)
    unidades: Mapped[list["Unidade"]] = relationship(
        "Unidade", 
        secondary="usuarios_unidades", 
        back_populates="users",
        lazy="selectin" # Carrega as unidades automaticamente ao buscar o usuário
    )

    # 3. Logs
    logs: Mapped[list["LogDocumento"]] = relationship("LogDocumento", back_populates="user")

    def __repr__(self):
        return f"<User {self.username} (Ativo: {self.is_active})>"