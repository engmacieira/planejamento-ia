from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    username: str
    email: EmailStr
    nome_completo: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
