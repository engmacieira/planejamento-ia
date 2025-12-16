from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.models.core.user_model import User
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class UserGestaoRepository(BaseRepository[User, dict, dict]):
    """
    Repositório de usuários específico do módulo de Gestão.
    Idealmente deve ser substituído pelo UserRepository do Core.
    Mantido para compatibilidade de importação durante a refatoração.
    """
    def __init__(self, db_session: AsyncSession):
        super().__init__(User, db_session)

    async def get_by_username(self, username: str) -> User | None:
        try:
            query = select(User).where(User.username == username, User.is_active == True)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Erro get_by_username UserGestao: {e}")
            return None
