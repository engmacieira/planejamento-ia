from typing import TYPE_CHECKING, List
from sqlalchemy import Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.planejamento.dfd_model import DFD
    from app.models.planejamento.item_etp_model import ItemETP
    from app.models.planejamento.etp_equipe_model import ETPEquipe
    from app.models.planejamento.etp_dotacao_model import ETPDotacao
    from app.models.planejamento.matriz_risco_model import MatrizRisco

class ETP(DefaultModel, Base): 
    """
    Estudo Técnico Preliminar (ETP) - Lei 14.133/2021.
    Documento que consolida demandas (DFDs) e avalia a viabilidade da contratação.
    """
    __tablename__ = "etps"

    # --- Conteúdo do Estudo (Campos ricos para IA preencher) ---
    descricao_necessidade: Mapped[str | None] = mapped_column(Text, nullable=True)
    previsao_pca: Mapped[str | None] = mapped_column(Text, nullable=True)
    requisitos_tecnicos: Mapped[str | None] = mapped_column(Text, nullable=True)
    motivacao_contratacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    levantamento_mercado: Mapped[str | None] = mapped_column(Text, nullable=True)
    justificativa_escolha: Mapped[str | None] = mapped_column(Text, nullable=True)
    descricao_solucao: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimativa_custos: Mapped[str | None] = mapped_column(Text, nullable=True)
    justificativa_parcelamento: Mapped[str | None] = mapped_column(Text, nullable=True)
    demonstrativo_resultados: Mapped[str | None] = mapped_column(Text, nullable=True)
    providencias_previas: Mapped[str | None] = mapped_column(Text, nullable=True)
    impactos_ambientais: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # --- Conclusão ---
    viabilidade: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    conclusao_viabilidade: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # --- Relacionamentos ---
    
    # 1. DFDs (Origem da Demanda)
    # A mágica acontece aqui: secondary="etp_dfds" busca a tabela de junção.
    # back_populates="etps" deve bater com o nome usado lá no DFD.
    dfds: Mapped[List["DFD"]] = relationship(
        "DFD", 
        secondary="etp_dfds", 
        back_populates="etps",
        lazy="selectin"
    )
    
    # 2. Tabelas Filhas (Dados consolidados ou específicos do ETP)
    itens: Mapped[List["ItemETP"]] = relationship("ItemETP", back_populates="etp", cascade="all, delete-orphan")
    equipe: Mapped[List["ETPEquipe"]] = relationship("ETPEquipe", back_populates="etp", cascade="all, delete-orphan")
    dotacoes: Mapped[List["ETPDotacao"]] = relationship("ETPDotacao", back_populates="etp", cascade="all, delete-orphan")
    
    # 3. Matriz de Risco (Geralmente 1 ETP tem 1 Matriz)
    matriz: Mapped["MatrizRisco"] = relationship("MatrizRisco", back_populates="etp", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ETP {self.id} (Viável: {self.viabilidade})>"