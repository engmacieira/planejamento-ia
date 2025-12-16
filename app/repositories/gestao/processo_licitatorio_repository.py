from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.planejamento.processo_licitatorio_model import ProcessoLicitatorio
from app.schemas.planejamento.processo_licitatorio_schema import ProcessoLicitatorioRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class ProcessoLicitatorioRepository(BaseRepository[ProcessoLicitatorio, ProcessoLicitatorioRequest, ProcessoLicitatorioRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ProcessoLicitatorio, db_session)

    async def get_by_numero(self, numero: str) -> ProcessoLicitatorio | None:
        try:
            query = select(ProcessoLicitatorio).where(ProcessoLicitatorio.numero == numero)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
             logger.exception(f"Erro ao buscar processo licitatorio '{numero}': {e}")
             return None

    async def get_or_create(self, numero: str) -> ProcessoLicitatorio:
        try:
            proc = await self.get_by_numero(numero)
            if proc: return proc
        except Exception:
            pass

        try:
            proc_req = ProcessoLicitatorioRequest(numero=numero)
            return await self.create(proc_req)
        except IntegrityError:
            await self.db_session.rollback()
            proc = await self.get_by_numero(numero)
            if proc: return proc
            raise
        except Exception as e:
            await self.db_session.rollback()
            raise e
