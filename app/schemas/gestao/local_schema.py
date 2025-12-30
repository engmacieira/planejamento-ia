from pydantic import BaseModel, ConfigDict

class LocalBase(BaseModel): 
    nome: str

class LocalRequest(LocalBase): 
    pass

class LocalResponse(LocalBase): 
    id: int

    model_config = ConfigDict(from_attributes=True)
