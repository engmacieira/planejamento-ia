from typing import Optional, Any
from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.base_model import DefaultModel

class LogAuditoria(DefaultModel, Base):
    """
    Tabela de Auditoria do Sistema (Audit Trail).
    Registra todas as ações críticas (CREATE, UPDATE, DELETE) realizadas pelos usuários.
    
    Regras de Negócio:
    - Imutabilidade: Logs não devem ser alterados (embora o banco permita, a aplicação não deve expor rota de update).
    - Rastreabilidade: Deve salvar o estado anterior e posterior do objeto alterado (Snapshot).
    """
    __tablename__ = "log_auditoria"

    # Quem fez?
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True, comment="Null caso seja ação do sistema")
    
    # O que fez?
    acao: Mapped[str] = mapped_column(String(50), nullable=False, comment="Ex: CREATE, UPDATE, DELETE, LOGIN, EXPORT")
    entidade: Mapped[str] = mapped_column(String(100), nullable=False, comment="Nome da tabela afetada (ex: Contrato)")
    entidade_id: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="ID do registro afetado")
    
    # O que mudou? (Snapshots)
    dados_anteriores: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True, comment="Estado antes da alteração")
    dados_novos: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True, comment="Estado depois da alteração")
    
    # Metadados Técnicos
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relacionamentos
    # Nota: Usamos string "User" para evitar import circular, pois User pode importar LogAuditoria no futuro
    usuario = relationship("User", foreign_keys=[usuario_id], lazy="selectin")

    def __repr__(self):
        return f"<LogAuditoria {self.acao} em {self.entidade} por User {self.usuario_id}>"