from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.gestao.tipo_documento_model import TipoDocumento
from app.schemas.gestao.tipo_documento_schema import TipoDocumentoRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class TipoDocumentoRepository(BaseRepository[TipoDocumento, TipoDocumentoRequest, TipoDocumentoRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(TipoDocumento, db_session)

    async def get_by_nome(self, nome: str) -> TipoDocumento | None:
        try:
            query = select(TipoDocumento).where(TipoDocumento.nome == nome)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
             logger.exception(f"Erro ao buscar tipo documento por nome '{nome}': {e}")
             return None

    async def get_or_create(self, nome: str) -> TipoDocumento:
        try:
            tipo = await self.get_by_nome(nome)
            if tipo:
                return tipo
        except Exception:
            pass

        try:
            tipo_req = TipoDocumentoRequest(nome=nome)
            return await self.create(tipo_req)
        except IntegrityError:
            await self.db_session.rollback()
            tipo = await self.get_by_nome(nome)
            if tipo: return tipo
            raise
        except Exception as e:
            await self.db_session.rollback()
            raise e
