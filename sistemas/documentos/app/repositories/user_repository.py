from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash
import sys

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate):
        try:
            hashed_password = get_password_hash(user_data.password)
            
            db_user = User(
                name=user_data.name,
                email=user_data.email,
                password_hash=hashed_password
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
            
        except Exception as e:
            self.db.rollback()
            # O print vai para o log do servidor
            print(f"Erro ao criar usuário: {e}", file=sys.stderr)
            raise e
            
    def get_by_email(self, email: str):
        """Busca usuário por email (útil para login e validação)"""
        return self.db.query(User).filter(User.email == email).first()