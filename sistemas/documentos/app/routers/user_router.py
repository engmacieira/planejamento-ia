from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schema import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.core.deps import get_user_repo

# Prefixo: todas as rotas aqui começam com /users
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(
    request: UserCreate, 
    repo: UserRepository = Depends(get_user_repo)
):
    # 1. Tentar criar
    try:
        new_user = repo.create_user(request)
        return new_user
    except Exception:
        # Se der erro (ex: email duplicado), o repo lançou Exception.
        # Aqui transformamos em erro HTTP 400 para o frontend entender.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Erro ao criar usuário. Email já cadastrado?"
        )