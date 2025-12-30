from pydantic import BaseModel, ConfigDict, Field


class UnidadeBase(BaseModel): 
    nome: str

class UnidadeRequest(UnidadeBase): 
    pass

class UnidadeResponse(UnidadeBase):
    id: int
    is_active: bool = Field(validation_alias="ativo", serialization_alias="is_active")

    model_config = ConfigDict(from_attributes=True)
