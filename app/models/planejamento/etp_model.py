from sqlalchemy import Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class ETP(Base):
    __tablename__ = "etps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
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
    viabilidade: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    conclusao_viabilidade: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    dfds: Mapped[list["DFD"]] = relationship("DFD", back_populates="etp")
    itens: Mapped[list["ItemETP"]] = relationship("ItemETP", back_populates="etp", cascade="all, delete-orphan")
    equipe: Mapped[list["ETPEquipe"]] = relationship("ETPEquipe", back_populates="etp", cascade="all, delete-orphan")
    dotacoes: Mapped[list["ETPDotacao"]] = relationship("ETPDotacao", back_populates="etp", cascade="all, delete-orphan")
    
    matriz: Mapped["MatrizRisco"] = relationship("MatrizRisco", back_populates="etp", uselist=False)
