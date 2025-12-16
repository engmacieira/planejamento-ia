from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.gestao.instrumento_model import InstrumentoContratual as Instrumento
from app.schemas.gestao.instrumento_schema import InstrumentoRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class InstrumentoRepository(BaseRepository[Instrumento, InstrumentoRequest, InstrumentoRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Instrumento, db_session)

    async def get_by_nome(self, nome: str) -> Instrumento | None:
        try:
            query = select(Instrumento).where(Instrumento.nome == nome)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
             logger.exception(f"Erro ao buscar instrumento por nome '{nome}': {e}")
             return None

    async def get_or_create(self, nome: str) -> Instrumento:
        try:
            inst = await self.get_by_nome(nome)
            if inst: return inst
        except Exception:
            pass

        try:
            inst_req = InstrumentoRequest(nome=nome)
            return await self.create(inst_req)
        except IntegrityError:
            await self.db_session.rollback()
            inst = await self.get_by_nome(nome)
            if inst: return inst
            raise
        except Exception as e:
            await self.db_session.rollback()
            raise e
