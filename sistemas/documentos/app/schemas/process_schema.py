from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProcessoBase(BaseModel):
    numero_dfd: str
    secretaria: str
    objeto: str
    valor_estimado: str
    valor_extenso: str
    
    # Opcionais
    dotacao: Optional[str] = None
    artigo: Optional[str] = None
    data1: Optional[str] = None
    data2: Optional[str] = None
    data3: Optional[str] = None
    data4: Optional[str] = None
    data5: Optional[str] = None

class ProcessoCreate(ProcessoBase):
    pass

class ProcessoResponse(ProcessoBase):
    id: int
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)