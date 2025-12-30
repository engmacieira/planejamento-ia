from datetime import date
from decimal import Decimal
from sqlalchemy import ForeignKey, String, Integer, Boolean, Date, Numeric, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel  

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.gestao.fornecedor_model import Fornecedor
    from app.models.gestao.instrumento_model import InstrumentoContratual
    from app.models.planejamento.categoria_model import Categoria
    from app.models.planejamento.modalidade_model import Modalidade

class Contrato(DefaultModel, Base): 
    __tablename__ = "contratos"

    numero_contrato: Mapped[str] = mapped_column(String(50), unique=True)
    ano_contrato: Mapped[int] = mapped_column(Integer)
    objeto: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    id_processo_licitatorio: Mapped[int] = mapped_column(ForeignKey("processos_licitatorios.id"))
    
    id_fornecedor: Mapped[int] = mapped_column(ForeignKey("fornecedores.id"))
    fornecedor: Mapped["Fornecedor"] = relationship("Fornecedor", back_populates="contratos", lazy="selectin")
    
    id_instrumento_contratual: Mapped[int | None] = mapped_column(ForeignKey("instrumentocontratual.id"), nullable=True)
    instrumento_contratual: Mapped["InstrumentoContratual"] = relationship("InstrumentoContratual", lazy="selectin")

    id_categoria: Mapped[int | None] = mapped_column(ForeignKey("categorias.id"), nullable=True)
    categoria: Mapped["Categoria"] = relationship("Categoria", lazy="selectin")

    id_modalidade: Mapped[int | None] = mapped_column(ForeignKey("modalidades.id"), nullable=True)
    modalidade: Mapped["Modalidade"] = relationship("Modalidade", lazy="selectin")

    data_assinatura: Mapped[date] = mapped_column(Date)
    data_inicio_vigencia: Mapped[date] = mapped_column(Date)
    data_fim_vigencia: Mapped[date] = mapped_column(Date)
    
    valor_total: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), default=0)
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())