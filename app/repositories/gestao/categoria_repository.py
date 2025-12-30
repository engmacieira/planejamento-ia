from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.planejamento.categoria_model import Categoria
from app.schemas.gestao.categoria_schema import CategoriaRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class CategoriaRepository(BaseRepository[Categoria, CategoriaRequest, CategoriaRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Categoria, db_session)

    async def get_by_nome(self, nome: str) -> Categoria | None:
        try:
            query = select(Categoria).where(Categoria.nome == nome)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
             logger.exception(f"Erro ao buscar categoria por nome '{nome}': {e}")
             return None

    async def get_or_create(self, nome: str) -> Categoria:
        try:
            cat = await self.get_by_nome(nome)
            if cat: return cat
        except Exception:
            pass

        try:
            cat_req = CategoriaRequest(nome=nome)
            return await self.create(cat_req)
        except IntegrityError:
            await self.db_session.rollback()
            cat = await self.get_by_nome(nome)
            if cat: return cat
            raise
        except Exception as e:
            await self.db_session.rollback()
            raise e
