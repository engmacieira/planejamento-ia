from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import date, datetime
from app.schemas.planejamento.cadastro_schema import ItemCatalogoResponse, DotacaoResponse, UnidadeRequisitanteResponse

# --- ITENS DO DFD ---
class DFDItemBase(BaseModel):
    catalogo_item_id: int 
    quantidade: float
    valor_unitario_estimado: float = 0.0

# --- EQUIPE E DOTAÇÃO ---
class DFDEquipeBase(BaseModel):
    agente_id: int
    papel: str

class DFDDotacaoBase(BaseModel):
    dotacao_id: int

# --- SCHEMAS DE RESPOSTA ---
class DFDItemResponse(DFDItemBase):
    id: int
    catalogo_item: Optional[ItemCatalogoResponse] = None 
    model_config = ConfigDict(from_attributes=True)

class DFDEquipeResponse(DFDEquipeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class DFDDotacaoResponse(DFDDotacaoBase):
    id: int
    dotacao: Optional[DotacaoResponse] = None
    model_config = ConfigDict(from_attributes=True)

# --- DFD PRINCIPAL ---
class DFDBase(BaseModel):
    # CORREÇÃO CRUCIAL: populate_by_name=True
    # Permite entrada via JSON ('objeto') E leitura via Banco ('descricao_sucinta')
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    # Campos base compartilhados
    numero: Optional[int] = None
    numero_protocolo_string: Optional[str] = None
    ano: int
    data_req: date
    unidade_requisitante_id: int 
    responsavel_id: int
    
    # Mapeamento Híbrido:
    # validation_alias="...": Ensina a ler do Banco de Dados
    # O nome do campo (objeto): É usado no JSON da API
    objeto: Optional[str] = Field(None, validation_alias="descricao_sucinta")
    justificativa: Optional[str] = Field(None, validation_alias="justificativa_necessidade")
    
    contratacao_vinculada: bool = False
    data_contratacao: Optional[str] = None
    etp_id: Optional[int] = None

# Criação
class DFDCreate(DFDBase):
    # Redefinimos para tornar obrigatório na criação, mantendo o alias da base
    objeto: str = Field(..., validation_alias="descricao_sucinta")
    justificativa: str = Field(..., validation_alias="justificativa_necessidade")
    
    # Listas Obrigatórias (podem ser vazias)
    itens: List[DFDItemBase]
    equipe: List[DFDEquipeBase]
    dotacoes: List[DFDDotacaoBase]

# Atualização
class DFDUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    numero: Optional[int] = None
    numero_protocolo_string: Optional[str] = None
    ano: Optional[int] = None
    data_req: Optional[date] = None
    
    unidade_requisitante_id: Optional[int] = None
    responsavel_id: Optional[int] = None
    
    objeto: Optional[str] = Field(None, validation_alias="descricao_sucinta")
    justificativa: Optional[str] = Field(None, validation_alias="justificativa_necessidade")
    
    itens: Optional[List[DFDItemBase]] = None
    equipe: Optional[List[DFDEquipeBase]] = None
    dotacoes: Optional[List[DFDDotacaoBase]] = None

# Leitura (Resposta)
class DFDResponse(DFDBase):
    id: int
    is_active: bool = Field(validation_alias="ativo", default=True)
    status: Optional[str] = "Rascunho" 
    created_at: Optional[datetime] = Field(None, validation_alias="data_criacao") 
    
    unidade_requisitante: Optional[UnidadeRequisitanteResponse] = None
    itens: List[DFDItemResponse] = []
    equipe: List[DFDEquipeResponse] = []
    dotacoes: List[DFDDotacaoResponse] = []
    
    # Herda o ConfigDict do DFDBase, então já tem from_attributes e populate_by_name

# Atualização de Preço em Lote
class DFDItemUpdatePrice(BaseModel):
    id: int
    valor_unitario_estimado: float