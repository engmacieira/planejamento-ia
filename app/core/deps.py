from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.core.user_model import User
from app.repositories.core.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

class MockService:
    """
    Classe placeholder para evitar o erro 'MockService não está definido'.
    Isso mantém a compatibilidade com funções antigas que você pediu para não remover.
    """
    def __init__(self, service_name: str):
        self.service_name = service_name

    async def execute(self, *args, **kwargs):
        return {"message": f"Service {self.service_name} called (Mock)"}

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Cria uma sessão assíncrona com o banco e garante o fechamento.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_user_repo(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)

def get_file_service():
    return MockService("FileService")

def get_document_service():
    return MockService("DocumentService")

def get_zip_service():
    return MockService("ZipService")

async def get_current_user(
    session: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Valida o token JWT e retorna o objeto User do banco de dados.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais não puderam ser validadas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_sub = payload.get("sub")
        
        if token_sub is None:
            raise credentials_exception
            
        user_id = int(token_sub)
        
    except (JWTError, ValidationError, ValueError):
        raise credentials_exception

    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
        
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="O usuário não tem privilégios suficientes"
        )
    return current_user