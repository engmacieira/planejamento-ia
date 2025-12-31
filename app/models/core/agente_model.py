from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.base_model import DefaultModel

class Agente(DefaultModel, Base):
    """
    Representa os Agentes Públicos responsáveis pelas etapas da licitação.
    Exemplos: Secretário Municipal, Fiscal de Contrato, Gestor, Ordenador de Despesa.
    
    Regras de Negócio:
    - CPF deve ser único (sem formatação).
    - 'ativo' indica se o funcionário ainda exerce função no órgão.
    - 'is_deleted' (herdado) indica se o registro foi excluído logicamente.
    """
    __tablename__ = "agentes_responsaveis"

    # Dados Pessoais
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, index=True, nullable=False, comment="Apenas números")
    
    # Contato
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Dados Funcionais
    matricula: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Matrícula interna do RH")
    cargo: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Ex: Secretário, Fiscal Técnico")
    
    # Status 
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, comment="Flag de Negócio: O servidor está ativo?")

    def __repr__(self):
        return f"<Agente {self.nome} ({self.cargo})>"