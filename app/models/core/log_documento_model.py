from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.core.user_model import User
    # Usamos string no relationship para evitar Circular Import com Planejamento
    # from app.models.planejamento.template_model import Template 

class LogDocumento(DefaultModel, Base):
    """
    Registra o histórico de geração de documentos via IA ou Templating.
    Diferente da tabela 'Anexo' (que guarda o arquivo final), esta tabela
    guarda o 'evento' de geração, útil para auditoria de custos e prompts.
    
    Regras de Negócio:
    - Deve registrar qual modelo de IA foi utilizado.
    - Deve registrar o consumo de tokens (se disponível) para cálculo de custo.
    """
    __tablename__ = "log_geracao_documentos"

    # O que foi gerado?
    nome_arquivo_gerado: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo_arquivo: Mapped[str] = mapped_column(String(50), default="docx", comment="docx, pdf, txt")
    
    # Metadados da IA (O Upgrade)
    ia_model: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Ex: gemini-pro-1.5")
    tokens_utilizados: Mapped[int | None] = mapped_column(Integer, default=0, comment="Custo da operação")
    parametros_usados: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Snapshot dos dados usados no prompt")

    # Relacionamentos
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="logs")
    
    # Template é opcional (pode ser geração livre)
    template_id: Mapped[int | None] = mapped_column(Integer, nullable=True) 
    # Removi a FK explicita para Template aqui para evitar acoplamento forte Core <-> Planejamento
    # A relação lógica existe, mas deixaremos solta no banco ou tratada via Service.

    def __repr__(self):
        return f"<LogDocumento {self.nome_arquivo_gerado} (Tokens: {self.tokens_utilizados})>"