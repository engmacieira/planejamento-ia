from sqlalchemy import String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Any

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.core.user_model import User

class Perfil(DefaultModel, Base):
    """
    Define os Perfis de Acesso (Roles) e suas Permissões (Scopes).
    
    Resolução do Débito Técnico (Integração com Core/Security):
    - Utilizamos o campo 'permissoes' (JSON) para mapear quais ações este perfil pode realizar.
    - O 'app/core/security.py' lerá este JSON para gerar o Token JWT com os scopes corretos.
    
    Exemplo de JSON em 'permissoes':
    {
        "scopes": ["usuarios:read", "contratos:write", "relatorios:view"],
        "nivel_aprovacao": 50000.00
    }
    """
    __tablename__ = "perfis"

    # Identificação
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="Ex: Admin, Gestor, Fiscal")
    descricao: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # O Coração do RBAC (Role Based Access Control)
    # Usamos JSON para permitir listas de scopes e configurações extras sem mudar o schema da tabela
    permissoes: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True, comment="Estrutura de permissões técnicas e limites")
    
    # Status de Negócio
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, comment="Flag de Negócio: Perfil disponível para uso?")

    # Relacionamentos
    users: Mapped[list["User"]] = relationship("User", back_populates="perfil")

    def __repr__(self):
        return f"<Perfil {self.nome} (Ativo: {self.ativo})>"