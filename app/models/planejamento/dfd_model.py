from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import String, Integer, ForeignKey, Text, Boolean, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.core.unidade_model import Unidade
    from app.models.core.user_model import User
    from app.models.planejamento.etp_model import ETP
    from app.models.planejamento.item_dfd_model import ItemDFD
    from app.models.planejamento.dfd_equipe_model import DFDEquipe
    from app.models.planejamento.dfd_dotacao_model import DFDDotacao

class DFD(DefaultModel, Base):
    """
    Documento de Formalização da Demanda (DFD).
    Base do planejamento.
    """
    __tablename__ = "dfds"

    # Regra: Unicidade de Número/Ano por Unidade
    __table_args__ = (
        UniqueConstraint('numero', 'ano', 'unidade_requisitante_id', name='uq_dfd_numero_ano_unidade'),
    )

    # Identificação
    numero: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    numero_protocolo_string: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    
    # Conteúdo
    descricao_sucinta: Mapped[str] = mapped_column(String(255), nullable=False, comment="Objeto da demanda")
    justificativa_necessidade: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_req: Mapped[date | None] = mapped_column(Date, nullable=True)
    
    # Relacionamentos (Pais)
    unidade_requisitante_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"), nullable=False)
    responsavel_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False) 
    
    # Status
    status: Mapped[str] = mapped_column(String(50), default='Rascunho')
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relacionamentos (Objetos)
    unidade_requisitante: Mapped["Unidade"] = relationship("Unidade", lazy="selectin")
    responsavel: Mapped["User"] = relationship("User", lazy="selectin")
    
    # --- MUDANÇA AQUI ---
    # Conexão com ETP agora é via tabela 'etp_dfds'.
    # Usamos 'etps' no plural, embora a regra de negócio diga que ele só entra em 1 ETP.
    # A constraint na tabela de junção garante a unicidade.
    etps: Mapped[List["ETP"]] = relationship(
        "ETP", 
        secondary="etp_dfds", 
        back_populates="dfds"
    )

    # Relacionamentos (Filhos)
    itens: Mapped[List["ItemDFD"]] = relationship("ItemDFD", back_populates="dfd", cascade="all, delete-orphan")
    equipe: Mapped[List["DFDEquipe"]] = relationship("DFDEquipe", back_populates="dfd", cascade="all, delete-orphan")
    dotacoes: Mapped[List["DFDDotacao"]] = relationship("DFDDotacao", back_populates="dfd", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DFD {self.numero}/{self.ano}>"