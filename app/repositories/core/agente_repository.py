from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.core.agente_model import Agente
from app.schemas.core.agente_schema import AgenteRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class AgenteRepository(BaseRepository[Agente, AgenteRequest, AgenteRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Agente, db_session)

    async def get_by_nome(self, nome: str) -> Agente | None:
        """Busca um Agente Responsável pelo nome exato."""
        try:
            query = select(Agente).where(Agente.nome == nome)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as error:
            logger.exception(f"Erro inesperado ao buscar agente por nome ('{nome}'): {error}")
            return None

    async def get_or_create(self, nome: str) -> Agente:
        """Busca um Agente pelo nome ou cria um novo se não existir."""
        try:
            agente = await self.get_by_nome(nome)
            if agente:
                return agente
        except Exception:
            logger.exception(f"Erro ao buscar agente '{nome}' em get_or_create. Tentando criar...")

        try:
            # Create assumes CreateSchema
            agente_req = AgenteRequest(nome=nome)
            return await self.create(agente_req)
        except IntegrityError:
            logger.warning(f"IntegrityError ao criar agente '{nome}' em get_or_create. Já existe. Buscando novamente.")
            await self.db_session.rollback()
            agente_existente = await self.get_by_nome(nome)
            if agente_existente:
                return agente_existente
            else:
                log_message = f"Erro INESPERADO ao buscar agente '{nome}' após conflito de inserção em get_or_create."
                logger.exception(log_message)
                raise Exception(log_message)
        except Exception as error:
            await self.db_session.rollback()
            logger.exception(f"Erro inesperado na criação do get_or_create para agente '{nome}': {error}")
            raise
