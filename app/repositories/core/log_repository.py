from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import sys
import logging

from app.models.core.log_documento_model import GenerationLog
from app.schemas.core.log_schema import LogCreate, LogUpdate
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class LogRepository(BaseRepository[GenerationLog, LogCreate, LogUpdate]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(GenerationLog, db_session)

    async def create_log(self, user_id: int, template_id: int, filename: str) -> GenerationLog:
        """
        Registra que um documento foi gerado.
        Mantém compatibilidade com assinatura antiga (agora async).
        """
        try:
            log_data = LogCreate(
                user_id=user_id,
                template_id=template_id,
                generated_filename=filename
            )
            return await self.create(log_data)
        except Exception as e:
            # Rollback handled in create, but we catch here to log specifically if needed
            logger.exception(f"Erro ao criar log via create_log: {e}")
            raise e

    async def list_by_user(self, user_id: int):
        """Histórico de gerações de um usuário específico."""
        try:
            query = select(GenerationLog).where(GenerationLog.user_id == user_id)
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"Erro ao listar logs do usuário {user_id}: {e}")
            return []
