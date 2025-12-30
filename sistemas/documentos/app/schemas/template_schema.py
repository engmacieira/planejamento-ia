from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TemplateBase(BaseModel):
    filename: str
    description: str | None = None

# Dados para criar (O path vem do sistema de arquivos, não do usuário direto)
class TemplateCreate(TemplateBase):
    pass 

# Dados para leitura (O que devolvemos para o front)
class TemplateResponse(TemplateBase):
    id: int
    path: str
    owner_id: int
    created_at: datetime
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)