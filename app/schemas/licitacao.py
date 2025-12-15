from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

# --- ItemDFD ---
class ItemDFDBase(BaseModel):
    id_catalogo_item: int
    numero_item: int
    quantidade: Decimal
    valor_unitario_estimado: Decimal

class ItemDFDCreate(ItemDFDBase):
    pass

class ItemDFD(ItemDFDBase):
    id: int
    id_dfd: int
    # valor_total_estimado: Optional[Decimal] # Computed/Generated

    model_config = ConfigDict(from_attributes=True)

# --- DFD ---
class DFDBase(BaseModel):
    numero: int
    ano: int
    descricao_sucinta: str
    justificativa_necessidade: Optional[str] = None
    id_unidade_requisitante: int

class DFDCreate(DFDBase):
    pass

class AFDUpdate(BaseModel):
    status: str

class DFD(DFDBase):
    id: int
    data_criacao: date
    status: str
    itens: List[ItemDFD] = []

    model_config = ConfigDict(from_attributes=True)

# --- Modalidade ---
class ModalidadeBase(BaseModel):
    nome: str
    sigla: Optional[str] = None
    fundamentacao_legal: Optional[str] = None

class Modalidade(ModalidadeBase):
    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)

# --- Processo Licitatorio ---
class ProcessoLicitatorioBase(BaseModel):
    id_dfd: int
    numero_processo: int
    ano_processo: int
    id_modalidade: int
    id_numero_modalidade: Optional[int] = None
    objeto: str
    valor_total_estimado: Optional[Decimal] = None
    data_abertura: Optional[date] = None
    data_homologacao: Optional[date] = None
    status: str = 'Em Andamento'

class ProcessoLicitatorioCreate(ProcessoLicitatorioBase):
    pass

class ProcessoLicitatorio(ProcessoLicitatorioBase):
    id: int
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)
