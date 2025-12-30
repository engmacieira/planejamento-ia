from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.core.unidade_model import Unidade
from app.schemas.core.unidade_schema import UnidadeRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class UnidadeRepository(BaseRepository[Unidade, UnidadeRequest, UnidadeRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Unidade, db_session)

    async def get_by_nome(self, nome: str) -> Unidade | None:
        try:
            query = select(Unidade).where(Unidade.nome == nome)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as error:
            logger.exception(f"Erro inesperado ao buscar unidade por nome ('{nome}'): {error}")
            return None

    async def get_or_create(self, nome: str) -> Unidade:
        try:
            unidade = await self.get_by_nome(nome)
            if unidade:
                return unidade
        except Exception:
            logger.exception(f"Erro ao buscar unidade '{nome}' em get_or_create. Tentando criar...")

        try:
            # Create assumes CreateSchema, so we construct one
            unidade_req = UnidadeRequest(nome=nome)
            return await self.create(unidade_req)
        except IntegrityError:
            logger.warning(f"IntegrityError ao criar unidade '{nome}' em get_or_create. Já existe. Buscando novamente.")
            await self.db_session.rollback()
            unidade_existente = await self.get_by_nome(nome)
            if unidade_existente:
                return unidade_existente
            else:
                log_message = f"Erro INESPERADO ao buscar unidade '{nome}' após conflito de inserção."
                logger.exception(log_message)
                raise Exception(log_message)
        except Exception as error:
            await self.db_session.rollback()
            logger.exception(f"Erro inesperado na criação do get_or_create para unidade '{nome}': {error}")
            raise
