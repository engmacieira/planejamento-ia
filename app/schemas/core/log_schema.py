from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LogBase(BaseModel):
    user_id: int
    template_id: int
    generated_filename: str

class LogCreate(LogBase):
    pass

class LogUpdate(BaseModel):
    # Logs usually aren't updated, but required for BaseRepository generics
    pass

# Schema apenas para leitura/resposta
class LogResponse(LogBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
