from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import logging

from app.models.gestao.item_model import ItemContrato
from app.schemas.gestao.item_schema import ItemRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class ItemRepository(BaseRepository[ItemContrato, ItemRequest, ItemRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ItemContrato, db_session)

    async def get_by_contrato(self, id_contrato: int) -> List[ItemContrato]:
        try:
            query = select(ItemContrato).where(ItemContrato.id_contrato == id_contrato, ItemContrato.ativo == True).order_by(ItemContrato.numero_item)
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except Exception as e:
             logger.error(f"Erro get_by_contrato: {e}")
             return []
