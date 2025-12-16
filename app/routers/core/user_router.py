from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.core.user_schema import UserCreate, UserResponse
from app.repositories.core.user_repository import UserRepository
from app.models.core.user_model import User

# CORREÇÃO: Importar de 'deps' para alinhar com o teste e usar get_current_user
from app.core.deps import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["Core - Users"])

# Helper para instanciar repositório
async def get_async_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    request: UserCreate, 
    repo: UserRepository = Depends(get_async_user_repo)
):
    try:
        new_user = await repo.create_user(request) # Assumindo repo async
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Erro ao criar usuário: {str(e)}"
        )

# ADIÇÃO: Rota /me para testar autenticação e obter dados do usuário logado
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário logado.
    Serve para testar se o token está sendo decodificado corretamente.
    """
    return current_user