from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

# --- Fornecedor ---
class FornecedorBase(BaseModel):
    razao_social: str
    nome_fantasia: Optional[str] = None
    cpf_cnpj: str
    email: Optional[str] = None
    telefone: Optional[str] = None

class FornecedorCreate(FornecedorBase):
    pass

class Fornecedor(FornecedorBase):
    id: int
    ativo: bool
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Instrumento Contratual ---
class InstrumentoContratualBase(BaseModel):
    nome: str

class InstrumentoContratualCreate(InstrumentoContratualBase):
    pass

class InstrumentoContratual(InstrumentoContratualBase):
    id: int
    ativo: bool
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Item Contrato ---
class ItemContratoBase(BaseModel):
    id_item_dfd: int
    numero_item: int
    marca: Optional[str] = None
    quantidade_contratada: Decimal
    valor_unitario_final: Decimal

class ItemContratoCreate(ItemContratoBase):
    pass

class ItemContrato(ItemContratoBase):
    id: int
    id_contrato: int
    valor_total_item: Optional[Decimal] = None # Computed

    model_config = ConfigDict(from_attributes=True)

# --- Contrato ---
class ContratoBase(BaseModel):
    numero_contrato: int
    ano_contrato: int
    
    id_processo_licitatorio: int
    id_numero_modalidade: int
    id_fornecedor: int
    id_instrumento_contratual: Optional[int] = None
    
    data_assinatura: date
    data_inicio_vigencia: date
    data_fim_vigencia: date
    
    valor_total: Optional[Decimal] = 0

class ContratoCreate(ContratoBase):
    itens: List[ItemContratoCreate]

class Contrato(ContratoBase):
    id: int
    ativo: bool
    data_criacao: datetime
    itens: List[ItemContrato] = []

    model_config = ConfigDict(from_attributes=True)

# --- AOCS ---
class AOCSBase(BaseModel):
    numero_aocs: str
    ano_aocs: int
    numero_pedido_externo: Optional[str] = None
    
    id_unidade_requisitante: int
    id_solicitante: Optional[int] = None
    id_agente_responsavel: Optional[int] = None
    id_local_entrega: Optional[int] = None
    id_dotacao: Optional[int] = None
    
    empenho: Optional[str] = None
    justificativa: Optional[str] = None

class AOCSCreate(AOCSBase):
    pass

class AOCSUpdateStatus(BaseModel):
    status: str

class AOCS(AOCSBase):
    id: int
    data_emissao: date
    status: str
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)
