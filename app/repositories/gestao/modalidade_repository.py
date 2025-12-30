from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.planejamento.modalidade_model import Modalidade
from app.schemas.gestao.modalidade_schema import ModalidadeRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class ModalidadeRepository(BaseRepository[Modalidade, ModalidadeRequest, ModalidadeRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Modalidade, db_session)

    async def get_by_nome(self, nome: str) -> Modalidade | None:
        try:
            query = select(Modalidade).where(Modalidade.nome == nome)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
             logger.exception(f"Erro ao buscar modalidade por nome '{nome}': {e}")
             return None

    async def get_or_create(self, nome: str) -> Modalidade:
        try:
            mod = await self.get_by_nome(nome)
            if mod: return mod
        except Exception:
            pass

        try:
            mod_req = ModalidadeRequest(nome=nome)
            return await self.create(mod_req)
        except IntegrityError:
            await self.db_session.rollback()
            mod = await self.get_by_nome(nome)
            if mod: return mod
            raise
        except Exception as e:
            await self.db_session.rollback()
            raise e
