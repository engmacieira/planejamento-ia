from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.core.user_model import User
# from app.repositories.user_repository import UserRepository # TODO: Create Repository later

# Security Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def create_access_token(user: User | None = None, data: dict | None = None) -> str:
    """
    Creates a JWT access token for the given user or data dictionary.
    """
    to_encode = {}
    
    if user:
        to_encode = {
            "sub": user.username,
            "id": user.id,
            # "nivel": user.nivel_acesso # TODO: Add back when Profile/Role model is stable
        }
    elif data:
        to_encode = data.copy()
    else:
        raise ValueError("create_access_token requires 'user' or 'data'")

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password using Werkzeug.
    """
    return check_password_hash(hashed_password, plain_password)

def get_password_hash(password: str) -> str:
    """
    Generates a password hash using Werkzeug.
    """
    return generate_password_hash(password)

# Dependency stub for getting current user (Needs user repo)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token_data = TokenData(username=username) 
    except JWTError:
        raise credentials_exception
        
    # TODO: Implement User Retrieval when Repository is ready
    # user = UserRepository.get_by_username(db, username=username)
    # if user is None:
    #     raise credentials_exception
    # return user
    return username # Temporary return until Repo is linked

def require_access_level(level: int):
    """
    Dependency factory to check if the current user has the required access level.
    TODO: Implement actual level check against User model.
    """
    def check_access(current_user: any = Depends(get_current_user)):
        # Logic to check user level would go here
        # if current_user.level < level: raise ...
        return current_user
    return check_access
