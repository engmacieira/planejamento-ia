from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.core.user_model import User
    from app.models.planejamento.etp_model import ETP

class TR(DefaultModel, Base):
    """
    Termo de Referência (TR).
    Documento puramente textual gerado (ou não) por IA, vinculado 1:1 a um ETP.
    
    Não possui numeração própria nesta fase; sua identificação é o ETP de origem.
    """
    __tablename__ = "trs"

    # Regra de Ouro: Um ETP só pode ter UM Termo de Referência.
    __table_args__ = (
        UniqueConstraint('etp_id', name='uq_tr_etp_vinculo_unico'),
    )

    # --- Vínculos ---
    # O "Pai" do TR. É daqui que sabemos de qual DFD/Unidade ele pertence.
    etp_id: Mapped[int] = mapped_column(ForeignKey("etps.id"), nullable=False)
    
    # Responsável pela elaboração deste documento específico (Login)
    responsavel_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    # Status de Controle
    status: Mapped[str] = mapped_column(String(50), default='Em Elaboração', comment="Rascunho, Gerado, Validado")

    # --- BLOCOS DE TEXTO (Campos para a IA preencher) ---
    # Todos nullable=True pois a IA pode gerar aos poucos.

    # 1. Introdução e Necessidade
    condicoes_gerais: Mapped[str | None] = mapped_column(Text, nullable=True)
    fundamentacao_necessidade: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # 2. O Objeto
    descricao_solucao: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Ciclo de vida e especificação")
    requisitos_contratacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    criterios_sustentabilidade: Mapped[str | None] = mapped_column(Text, nullable=True)
    amostra: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Exigência de amostra/prova de conceito")

    # 3. Execução
    modelo_execucao: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Execução do objeto")
    forma_execucao_selecao: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # 4. Gestão e Fiscalização
    modelo_gestao: Mapped[str | None] = mapped_column(Text, nullable=True)
    criterios_recebimento: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # 5. Financeiro
    procedimento_liquidacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    criterios_pagamento: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # 6. Habilitação (Requisitos do Fornecedor)
    exigencias_habilitacao: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Visão geral da habilitação")
    qualificacao_juridica: Mapped[str | None] = mapped_column(Text, nullable=True)
    regularidade_fiscal: Mapped[str | None] = mapped_column(Text, nullable=True)
    qualificacao_tecnica: Mapped[str | None] = mapped_column(Text, nullable=True)
    qualificacao_economico_financeira: Mapped[str | None] = mapped_column(Text, nullable=True)
    declaracoes_complementares: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # 7. Obrigações
    obrigacoes_contratante: Mapped[str | None] = mapped_column(Text, nullable=True)
    obrigacoes_contratada: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Acesso aos dados do ETP (Itens, Dotação, Equipe são lidos daqui)
    etp: Mapped["ETP"] = relationship("ETP", lazy="selectin")

    def __repr__(self):
        return f"<TR (Vinculado ao ETP {self.etp_id}) - Status: {self.status}>"