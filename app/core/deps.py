from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.database import get_db
from app.core.config import settings
from app.core.security import ALGORITHM, SECRET_KEY, oauth2_scheme
from app.models.core.user_model import User

# TODO: Import Repositories and Services when they are migrated
# from app.repositories.user_repository import UserRepository
# from app.repositories.template_repository import TemplateRepository
# from app.repositories.log_repository import LogRepository
# from app.services.file_service import FileService 
# from app.services.document_service import DocumentService
# from app.services.zip_service import ZipService

# Mock classes for dependencies that don't exist yet to prevent ImportErrors
class MockService:
    def __init__(self, name): self.name = name

# --- Repository Injectors (Stubs) ---
# def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
#     return UserRepository(db)

# def get_template_repo(db: Session = Depends(get_db)) -> TemplateRepository:
#     return TemplateRepository(db)

# def get_log_repo(db: Session = Depends(get_db)) -> LogRepository:
#     return LogRepository(db)

# --- Service Injectors (Stubs) ---
def get_file_service():
    """Injeta a instância do serviço de arquivos (Stub)."""
    return MockService("FileService")

def get_document_service():
    """Injeta a instância do serviço de leitura de documentos Word (Stub)."""
    return MockService("DocumentService")

def get_zip_service():
    return MockService("ZipService")

# --- Auth Dependency ---
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Validates token and returns current user.
    WARNING: Currently returns only the extracted email/username string 
    because UserRepository is not yet available in app/repositories.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou expiradas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Tenta decodificar o token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # 2. Busca o usuário no banco (TODO: Uncomment when Repo is ready)
    # repo = UserRepository(db)
    # user = repo.get_by_email(email=username) # OR get_by_username depending on model
    
    # if user is None:
    #     raise credentials_exception
    
    # return user
    return {"username": username, "msg": "User object pending Repo migration"}
