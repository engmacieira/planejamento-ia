import pytest
from fastapi import HTTPException
from app.core.deps import get_log_repo, get_current_user
from app.repositories.log_repository import LogRepository
from app.core.security import create_access_token
from app.schemas.user_schema import UserCreate
from app.repositories.user_repository import UserRepository

# --- TESTE 1: LogRepository (Simples) ---
def test_get_log_repo_dependency(db_session):
    """
    Testa se o injetor de dependência retorna a classe correta.
    Cobre a linha: return LogRepository(db)
    """
    repo = get_log_repo(db_session)
    assert isinstance(repo, LogRepository)

# --- TESTE 2: Erros de Autenticação (O Grosso do deps.py) ---

def test_get_current_user_invalid_token(db_session):
    """
    Cenário: Token malformado (lixo).
    Cobre: except JWTError -> raise credentials_exception
    """
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token="token_invalido_lixo", db=db_session)
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Credenciais inválidas ou expiradas"

def test_get_current_user_valid_token_but_user_not_found(db_session):
    """
    Cenário: Token é válido (assinatura ok), mas o email lá dentro
    não existe no banco de dados (ex: usuário foi deletado).
    Cobre: if user is None -> raise credentials_exception
    """
    # 1. Gera um token válido para um fantasma
    token = create_access_token(data={"sub": "fantasma@teste.com"})
    
    # 2. Tenta autenticar
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token=token, db=db_session)
        
    assert excinfo.value.status_code == 401

def test_get_current_user_token_without_sub(db_session):
    """
    Cenário: Token válido, mas sem o campo 'sub' (email).
    Cobre: if email is None -> raise credentials_exception
    """
    # 1. Gera token com payload incompleto (sem 'sub')
    token = create_access_token(data={"outro_campo": "nada_a_ver"})
    
    # 2. Tenta autenticar
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token=token, db=db_session)
        
    assert excinfo.value.status_code == 401

# --- TESTE EXTRA: Caminho Feliz (Só para garantir) ---
def test_get_current_user_success(db_session):
    # Cria usuário
    repo = UserRepository(db_session)
    repo.create_user(UserCreate(name="Real", email="real@auth.com", password="123"))
    
    # Gera token
    token = create_access_token(data={"sub": "real@auth.com"})
    
    # Chama a dependência
    user = get_current_user(token=token, db=db_session)
    
    assert user.email == "real@auth.com"