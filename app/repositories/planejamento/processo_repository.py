from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.models.planejamento.processo_documento_model import ProcessoDocumento as Processo
from app.schemas.planejamento.processo_schema import ProcessoCreate
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class ProcessoRepository(BaseRepository[Processo, ProcessoCreate, ProcessoCreate]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Processo, db_session)

    async def create_processo(self, schema: ProcessoCreate, owner_id: int) -> Processo:
        try:
            db_processo = Processo(
                **schema.model_dump(), 
                owner_id=owner_id
            )
            self.db_session.add(db_processo)
            await self.db_session.commit()
            await self.db_session.refresh(db_processo)
            return db_processo
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro create processo: {e}")
            raise e

    async def list_by_user(self, owner_id: int):
        result = await self.db_session.execute(select(Processo).where(Processo.owner_id == owner_id))
        return result.scalars().all()
