from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.schemas.token_schema import Token

router = APIRouter(tags=["Auth"])

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Rota de Login Padrão OAuth2.
    O form_data traz: username (que usaremos como email) e password.
    """
    repo = UserRepository(db)
    
    # 1. Busca o usuário pelo email (O campo vem como 'username' no form padrão)
    user = repo.get_by_email(form_data.username)
    
    # 2. Verifica se usuário existe E se a senha bate
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Se passou, gera o Token JWT
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}