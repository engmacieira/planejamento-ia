from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.gestao.dotacao_model import Dotacao
from app.schemas.gestao.dotacao_schema import DotacaoRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class DotacaoRepository(BaseRepository[Dotacao, DotacaoRequest, DotacaoRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Dotacao, db_session)

    async def get_by_descricao(self, descricao: str) -> Dotacao | None:
        try:
            query = select(Dotacao).where(Dotacao.descricao == descricao)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
             logger.exception(f"Erro ao buscar dotação por descrição: {e}")
             return None

    async def get_or_create(self, descricao: str) -> Dotacao:
        try:
            dotacao = await self.get_by_descricao(descricao)
            if dotacao:
                return dotacao
        except Exception:
            pass

        try:
            # Create via BaseRepository
            dotacao_req = DotacaoRequest(descricao=descricao)
            return await self.create(dotacao_req)
        except IntegrityError:
            await self.db_session.rollback()
            dotacao = await self.get_by_descricao(descricao)
            if dotacao: return dotacao
            raise
        except Exception as e:
            await self.db_session.rollback()
            raise e
