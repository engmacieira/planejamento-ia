from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

# CORREÇÃO: Importar de 'deps' para que o override do teste funcione
from app.core.deps import get_db 
from app.repositories.core.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.schemas.core.token_schema import Token

router = APIRouter(tags=["Core - Auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Rota de Login Padrão OAuth2 (Versão Async).
    """
    repo = UserRepository(db)
    
    # 1. Busca assíncrona (await é obrigatório aqui)
    user = await repo.get_by_email(form_data.username)
    
    # 2. Verifica se usuário existe e senha confere
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Gera Token usando o ID
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}