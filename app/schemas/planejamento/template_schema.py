from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TemplateBase(BaseModel):
    filename: str
    description: Optional[str] = None

class TemplateCreate(TemplateBase):
    pass

class TemplateResponse(TemplateBase):
    id: int
    path: str
    owner_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
