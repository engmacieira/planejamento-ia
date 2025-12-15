from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.repositories.user_repository import UserRepository
from app.repositories.template_repository import TemplateRepository
from app.repositories.log_repository import LogRepository
from app.models.user_model import User

from app.services.file_service import FileService 
from app.services.document_service import DocumentService
from app.services.zip_service import ZipService

# O FastAPI usa isso para saber onde procurar o token (na URL /token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Repositories (Já existiam) ---
def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_template_repo(db: Session = Depends(get_db)) -> TemplateRepository:
    return TemplateRepository(db)

def get_log_repo(db: Session = Depends(get_db)) -> LogRepository:
    return LogRepository(db)

def get_file_service() -> FileService:
    """Injeta a instância do serviço de arquivos."""
    return FileService()

def get_document_service() -> DocumentService:
    """Injeta a instância do serviço de leitura de documentos Word."""
    return DocumentService()

def get_zip_service() -> ZipService:
    return ZipService()

# --- O NOVO GUARDA-COSTAS ---
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou expiradas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Tenta decodificar o token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # 2. Busca o usuário no banco
    repo = UserRepository(db)
    user = repo.get_by_email(email)
    
    if user is None:
        raise credentials_exception
        
    return user