from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Boolean, Numeric, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.core.unidade_model import Unidade

class Dotacao(DefaultModel, Base):
    """
    Representa a Dotação Orçamentária Disponível.
    Fonte de recurso financeira para as despesas.
    """
    __tablename__ = "dotacoes"  # Corrigido para PLURAL

    # Regra de Ouro: No mesmo ano (exercício) e na mesma secretaria, 
    # não pode haver repetição da mesma ficha ou código.
    __table_args__ = (
        UniqueConstraint('exercicio', 'unidade_id', 'numero_ficha', name='uq_dotacao_exercicio_unidade_ficha'),
        CheckConstraint("exercicio >= 2000", name="check_exercicio_valido"),
    )

    # Identificação Orçamentária
    exercicio: Mapped[int] = mapped_column(Integer, nullable=False, comment="Ano do Orçamento (ex: 2025)")
    numero_ficha: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Número da ficha no sistema contábil")
    
    # Classificação Funcional Programática (A string longa: 10.301.0001.2001...)
    codigo_dotacao: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="Ex: Manutenção da Atenção Básica")
    
    # Fonte de Recurso (Ex: 1.500.1001 - Recurso Próprio)
    fonte_recurso: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Vínculo com a Secretaria (O Dono do Dinheiro)
    # Isso impede que a Educação gaste verba da Saúde
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"), nullable=False)
    unidade: Mapped["Unidade"] = relationship("Unidade", lazy="selectin")

    # Saldos
    saldo_inicial: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0.00)
    saldo_atual: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0.00, comment="Atualizado via triggers ou services")
    
    # Status
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"<Dotacao {self.exercicio} - Ficha {self.numero_ficha} (R$ {self.saldo_atual})>"