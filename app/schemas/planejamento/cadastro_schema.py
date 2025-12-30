from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

# --- Unidade Requisitante (Antiga Secretaria) ---
class UnidadeRequisitanteBase(BaseModel):
    nome: str
    sigla: Optional[str] = None
    codigo_administrativo: Optional[str] = None
    unidade_superior_id: Optional[int] = None

class UnidadeRequisitanteResponse(UnidadeRequisitanteBase):
    id: int
    # CORREÇÃO: Mapeia 'ativo' (banco) para 'is_active' (schema)
    is_active: bool = Field(validation_alias="ativo") 
    model_config = ConfigDict(from_attributes=True)

# --- Agente Responsável ---
class AgenteResponsavelBase(BaseModel):
    nome: str
    matricula: Optional[str] = None
    cargo: Optional[str] = None
    email: Optional[str] = None
    unidade_id: Optional[int] = None

class AgenteResponsavelResponse(AgenteResponsavelBase):
    id: int
    # CORREÇÃO: Mapeia 'ativo' (banco) para 'is_active' (schema)
    is_active: bool = Field(validation_alias="ativo")
    model_config = ConfigDict(from_attributes=True)

# --- Item Catalogo (Unificado) ---
class ItemCatalogoBase(BaseModel):
    codigo: Optional[str] = None
    
    # Mapeia 'nome_item' (do banco) para 'nome' (do schema/frontend)
    nome: str = Field(validation_alias="nome_item")
    
    descricao: Optional[str] = None
    unidade_medida: str
    tipo: str = "material" 
    valor_referencia: Optional[float] = 0.0
    
    # populate_by_name=True permite que o frontend envie {'nome': '...'} na criação
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class ItemCatalogoCreate(ItemCatalogoBase):
    pass

class ItemCatalogoResponse(ItemCatalogoBase):
    id: int
    # CORREÇÃO: Mapeia 'ativo' (banco) para 'is_active' (schema)
    is_active: bool = Field(validation_alias="ativo")
    model_config = ConfigDict(from_attributes=True)

# --- Dotação Orçamentária ---
class DotacaoBase(BaseModel):
    ano: int
    codigo: str
    descricao: str
    valor_total: float = 0.0
    valor_disponivel: float = 0.0

class DotacaoResponse(DotacaoBase):
    id: int
    # CORREÇÃO: Mapeia 'ativo' (banco) para 'is_active' (schema)
    is_active: bool = Field(validation_alias="ativo")
    model_config = ConfigDict(from_attributes=True)