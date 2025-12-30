from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProcessoLicitatorioBase(BaseModel): 
    # Usado para passar a string completa se necessário (legado)
    numero: Optional[str] = None 
    
    # Campos reais do Model
    numero_processo: Optional[int] = None
    ano_processo: Optional[int] = None
    objeto: Optional[str] = None
    id_dfd: Optional[int] = None
    id_modalidade: Optional[int] = None
    status: Optional[str] = None

class ProcessoLicitatorioRequest(ProcessoLicitatorioBase): 
    pass

# CORREÇÃO AQUI: Definindo a classe que estava faltando
class ProcessoLicitatorioCreateRequest(ProcessoLicitatorioBase):
    pass

class ProcessoLicitatorioResponse(ProcessoLicitatorioBase): 
    id: int
    model_config = ConfigDict(from_attributes=True)