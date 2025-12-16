from pydantic import BaseModel, ConfigDict

class FornecedorBase(BaseModel):
    razao_social: str
    nome_fantasia: str | None = None
    cpf_cnpj: str
    email: str | None = None
    telefone: str | None = None

class FornecedorRequest(FornecedorBase):
    pass

class FornecedorResponse(FornecedorBase):
    
    model_config = ConfigDict(from_attributes=True)
