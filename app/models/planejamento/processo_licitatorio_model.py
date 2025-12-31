from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Text, Numeric, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel 

if TYPE_CHECKING:
    from app.models.planejamento.tr_model import TR
    from app.models.planejamento.modalidade_model import Modalidade
    from app.models.planejamento.numero_modalidade_model import NumeroModalidade

class ProcessoLicitatorio(DefaultModel, Base): 
    """
    Registro do Processo Licitatório.
    Armazena os dados finais da licitação para fins de histórico e vínculo contratual.
    Não gerencia a disputa (lances), apenas o resultado.
    """
    __tablename__ = "processos_licitatorios"

    # Regra: Não pode haver dois processos com o mesmo número/ano.
    # (Adicionei 'numero_modalidade_id' na constraint caso queira garantir unicidade do Edital também)
    __table_args__ = (
        UniqueConstraint('numero_processo', 'ano_processo', name='uq_processo_numero_ano'),
    )

    # --- Vínculo com o Planejamento ---
    tr_id: Mapped[int] = mapped_column(ForeignKey("trs.id"), nullable=False, unique=True)
    tr: Mapped["TR"] = relationship("TR", lazy="selectin")
    
    # --- Identificação Administrativa ---
    numero_processo: Mapped[int] = mapped_column(Integer, nullable=False)
    ano_processo: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # --- Identificação da Modalidade (O "Edital") ---
    # Qual a regra usada? (Pregão, Dispensa...)
    modalidade_id: Mapped[int] = mapped_column(ForeignKey("modalidades.id"), nullable=False)
    modalidade: Mapped["Modalidade"] = relationship("Modalidade", lazy="selectin")
    
    # O número específico gerado (Ex: Pregão 01/2025)
    # Vincula com a tabela de controle de numeração que criamos antes.
    numero_modalidade_id: Mapped[int | None] = mapped_column(ForeignKey("numeros_modalidades.id"), nullable=True)
    numero_modalidade_obj: Mapped["NumeroModalidade"] = relationship("NumeroModalidade", lazy="selectin")
    
    # --- Dados de Resultado ---
    objeto: Mapped[str] = mapped_column(Text, nullable=False)
    
    valor_total_estimado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    valor_total_homologado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True, comment="Valor final após a disputa")
    
    # Datas importantes para o Contrato
    data_abertura: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_homologacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default='Em Andamento')
    
    # data_criacao removida (Já existe no DefaultModel)

    def __repr__(self):
        return f"<Processo {self.numero_processo}/{self.ano_processo}>"