from pydantic import BaseModel, EmailStr, ConfigDict

# Base: Campos comuns
class UserBase(BaseModel):
    name: str
    email: EmailStr

# Create: O que o usuário manda (tem senha)
class UserCreate(UserBase):
    password: str

# Response: O que devolvemos (NÃO tem senha, tem ID e datas)
class UserResponse(UserBase):
    id: int
    is_active: bool = True
    is_deleted: bool = False

    # Configuração V2 para ler do ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)