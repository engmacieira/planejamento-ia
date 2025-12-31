from typing import TYPE_CHECKING, Any, Dict
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel

if TYPE_CHECKING:
    from app.models.core.user_model import User
    from app.models.planejamento.processo_licitatorio_model import ProcessoLicitatorio

class ProcessoDocumento(DefaultModel, Base):
    """
    Tabela Auxiliar para Geração de Documentos (Minutas).
    Funciona como um 'Armazém de Variáveis' que o usuário preenche na hora
    de gerar a Capa do Processo, o Edital ou o Contrato.
    
    Linkamos ao ProcessoLicitatorio para ter acesso a toda a árvore de dados:
    (Processo -> TR -> ETP -> DFD).
    """
    __tablename__ = "processo_documentos" # Renomeado para evitar conflito com 'processos_licitatorios'

    # --- Vínculo Principal ---
    # Ao invés do DFD (início), ligamos ao Processo (fim da cadeia de planejamento).
    processo_licitatorio_id: Mapped[int] = mapped_column(ForeignKey("processos_licitatorios.id"), nullable=False)
    
    # Quem preencheu esses dados para a geração do documento?
    responsavel_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    # --- Campos de Preenchimento (Template) ---
    
    # Ex: "Lei 14.133/21, Art. 75, Inciso II" (Justificativa legal impressa na capa)
    fundamentacao_legal_artigo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # CAMPO PODEROSO: JSON para substituir data1, data2, data3...
    # Aqui guardamos qualquer variável extra que o template .doc exija.
    # Ex: {"data_assinatura": "10/01/2025", "numero_portaria": "123/2024", "local": "São Paulo"}
    variaveis_modelo: Mapped[Dict[str, Any] | None] = mapped_column(JSON, nullable=True, comment="Dicionário com dados variáveis para preencher as minutas")

    # --- Relacionamentos ---
    
    processo_licitatorio: Mapped["ProcessoLicitatorio"] = relationship("ProcessoLicitatorio", lazy="selectin")
    responsavel: Mapped["User"] = relationship("User", lazy="selectin")

    # --- Helpers (Propriedades para facilitar a vida do Gerador de Docs) ---
    
    @property
    def objeto_formatado(self) -> str:
        """Busca o objeto lá no Processo -> TR -> ETP"""
        if self.processo_licitatorio and self.processo_licitatorio.tr:
            return self.processo_licitatorio.tr.objeto
        return "Objeto não definido"

    @property
    def numero_processo_completo(self) -> str:
        """Retorna '001/2025' pronto para impressão"""
        if self.processo_licitatorio:
            return f"{self.processo_licitatorio.numero_processo}/{self.processo_licitatorio.ano_processo}"
        return "S/N"