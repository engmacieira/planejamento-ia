from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import sys
import logging

from app.models.core.user_model import User
from app.schemas.core.user_schema import UserCreate, UserBase
from app.repositories.base_repository import BaseRepository
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)

class UserRepository(BaseRepository[User, UserCreate, UserBase]): # Using UserBase as UpdateSchema for now
    def __init__(self, db_session: AsyncSession):
        super().__init__(User, db_session)

    async def create(self, user_data: UserCreate) -> User:
        """
        Cria usuário com hash de senha.
        Overrides método create do BaseRepository.
        """
        try:
            hashed_password = get_password_hash(user_data.password)
            
            db_user = User(
                username=user_data.username,
                nome_completo=user_data.nome_completo,
                email=user_data.email,
                password_hash=hashed_password
                # id_perfil defaults to None or handled elsewhere?
            )
            
            self.db_session.add(db_user)
            await self.db_session.commit()
            await self.db_session.refresh(db_user)
            return db_user
            
        except Exception as e:
            await self.db_session.rollback()
            logger.exception(f"Erro ao criar usuário: {e}")
            raise e
            
    async def get_by_email(self, email: str) -> User | None:
        """Busca usuário por email (útil para login e validação)"""
        try:
            query = select(User).where(User.email == email)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.exception(f"Erro ao buscar usuário por email {email}: {e}")
            return None
