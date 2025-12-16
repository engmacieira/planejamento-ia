from datetime import date
from decimal import Decimal
from sqlalchemy import ForeignKey, String, Integer, Boolean, Date, Numeric, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
# Imports for string forward references are not strictly needed at runtime if using "ClassName" string, but good for clarity or TYPE_CHECKING
# Keeping it simple with string refs as used in relationship arguments.

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.gestao.fornecedor_model import Fornecedor
    from app.models.gestao.instrumento_model import InstrumentoContratual
    from app.models.planejamento.categoria_model import Categoria
    from app.models.planejamento.modalidade_model import Modalidade

class Contrato(Base): 
    __tablename__ = "contratos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Identificação do Contrato
    numero_contrato: Mapped[str] = mapped_column(String(50), unique=True)
    ano_contrato: Mapped[int] = mapped_column(Integer)
    objeto: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # Hierarquia: Processo Licitatório
    # Aponta para tabela processos_licitatorios
    id_processo_licitatorio: Mapped[int] = mapped_column(ForeignKey("processos_licitatorios.id"))
    
    # A Modalidade Específica
    id_numero_modalidade: Mapped[int] = mapped_column(ForeignKey("numeros_modalidade.id"))
    
    # Quem?
    id_fornecedor: Mapped[int] = mapped_column(ForeignKey("fornecedores.id"))
    fornecedor: Mapped["Fornecedor"] = relationship("Fornecedor", back_populates="contratos", lazy="selectin")
    
    # Classificação
    # Classificação
    # Nota: SQL referencia 'instrumentocontratual' (singular, tudo junto)
    id_instrumento_contratual: Mapped[int | None] = mapped_column(ForeignKey("instrumentocontratual.id"), nullable=True)
    instrumento_contratual: Mapped["InstrumentoContratual"] = relationship("InstrumentoContratual", lazy="selectin")

    id_categoria: Mapped[int | None] = mapped_column(ForeignKey("categorias.id"), nullable=True)
    categoria: Mapped["Categoria"] = relationship("Categoria", lazy="selectin")

    # Modalidade Generic (if used separate from NumeroModalidade or just redundancy?)
    # Repo sets id_modalidade.
    id_modalidade: Mapped[int | None] = mapped_column(ForeignKey("modalidades.id"), nullable=True)
    modalidade: Mapped["Modalidade"] = relationship("Modalidade", lazy="selectin")

    # Vigência
    data_assinatura: Mapped[date] = mapped_column(Date)
    data_inicio_vigencia: Mapped[date] = mapped_column(Date)
    data_fim_vigencia: Mapped[date] = mapped_column(Date)
    
    valor_total: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), default=0)
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())

    @property
    def data_inicio(self) -> date:
        return self.data_inicio_vigencia

    @property
    def data_fim(self) -> date:
        return self.data_fim_vigencia
