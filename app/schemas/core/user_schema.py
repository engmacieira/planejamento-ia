from pydantic import BaseModel, EmailStr, ConfigDict

# Base: Campos comuns
class UserBase(BaseModel):
    username: str
    nome_completo: str
    email: EmailStr

# Create: O que o usuário manda (tem senha)
class UserCreate(UserBase):
    password: str

UserCreateRequest = UserCreate

# Response: O que devolvemos (NÃO tem senha, tem ID e datas)
class UserResponse(UserBase):
    id: int
    is_active: bool = True
    
    # Configuração V2 para ler do ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

class UserChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    nome_completo: str | None = None
    password: str | None = None
    is_active: bool | None = None
    cpf: str | None = None
    telefone: str | None = None

UserUpdateRequest = UserUpdate

class UserAdminResponse(UserResponse):
    cpf: str | None = None
    telefone: str | None = None
    id_perfil: int | None = None

class UserFilter(BaseModel):
    username: str | None = None
    email: str | None = None
    ativo: bool | None = None
    
    model_config = ConfigDict(from_attributes=True)
