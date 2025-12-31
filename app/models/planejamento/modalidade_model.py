from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.base_model import DefaultModel

class Modalidade(DefaultModel, Base):
    """
    Catálogo de Modalidades de Licitação e Contratação Direta.
    Baseado na Lei 14.133/2021 (Nova Lei de Licitações).
    
    Exemplos: 
    - Pregão
    - Concorrência
    - Diálogo Competitivo
    - Dispensa de Licitação
    - Inexigibilidade
    """
    __tablename__ = "modalidades"

    # Regra: Não podem existir duas modalidades com o mesmo nome ou sigla.
    __table_args__ = (
        UniqueConstraint('nome', name='uq_modalidade_nome'),
        UniqueConstraint('sigla', name='uq_modalidade_sigla'),
    )

    # Identificação
    nome: Mapped[str] = mapped_column(String(100), nullable=False, comment="Ex: Pregão Eletrônico")
    sigla: Mapped[str] = mapped_column(String(20), nullable=False, comment="Ex: PE, CONC, DISP")
    
    # Configuração Legal
    fundamento_legal: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Artigo da lei que define esta modalidade")
    
    # Regras de Negócio (Flags para o Frontend/Backend saberem como lidar)
    permite_disputa: Mapped[bool] = mapped_column(Boolean, default=True, comment="Se True, habilita fase de lances (Ex: Pregão)")
    eletronica: Mapped[bool] = mapped_column(Boolean, default=True, comment="Se a modalidade ocorre em ambiente virtual")
    
    # Status do Cadastro
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"<Modalidade {self.sigla} - {self.nome}>"