from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.gestao.local_model import Local
from app.schemas.gestao.local_schema import LocalRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class LocalRepository(BaseRepository[Local, LocalRequest, LocalRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Local, db_session)

    async def get_by_nome(self, nome: str) -> Local | None:
        try:
            query = select(Local).where(Local.nome == nome)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
             logger.exception(f"Erro ao buscar local de entrega por nome '{nome}': {e}")
             return None

    async def get_or_create(self, nome: str) -> Local:
        try:
            local = await self.get_by_nome(nome)
            if local:
                return local
        except Exception:
            pass

        try:
            # Create via BaseRepository logic (assuming Schema matches Model)
            local_req = LocalRequest(nome=nome)
            return await self.create(local_req)
        except IntegrityError:
            await self.db_session.rollback()
            local = await self.get_by_nome(nome)
            if local: return local
            raise
        except Exception as e:
            await self.db_session.rollback()
            raise e
