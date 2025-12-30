from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Schema apenas para leitura/resposta
class LogResponse(BaseModel):
    id: int
    generated_filename: str
    user_id: int
    template_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)