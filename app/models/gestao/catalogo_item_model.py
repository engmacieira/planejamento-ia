from datetime import date
from sqlalchemy import String, Boolean, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.base_model import DefaultModel  

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.planejamento.subgrupo_model import Subgrupo

class CatalogoItem(DefaultModel, Base): 
    __tablename__ = "catalogo_itens"
    
    id_subgrupo: Mapped[int] = mapped_column(ForeignKey("subgrupos.id"))
    subgrupo: Mapped["Subgrupo"] = relationship("Subgrupo", lazy="selectin")
    
    nome_item: Mapped[str] = mapped_column(String(255))
    unidade_medida: Mapped[str] = mapped_column(String(50))
    tipo: Mapped[str] = mapped_column(String(20)) 
    
    codigo_catmat_catser: Mapped[str | None] = mapped_column(String(50), nullable=True)
    numero_sequencial_taxonomia: Mapped[str] = mapped_column(String(4))
    codigo_identificacao_completo: Mapped[str | None] = mapped_column(String(10), unique=True, nullable=True)
    
    descricao_detalhada: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    data_criacao: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())