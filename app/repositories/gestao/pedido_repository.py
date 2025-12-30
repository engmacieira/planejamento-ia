from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.models.gestao.pedido_model import Pedido
from app.schemas.gestao.pedido_schema import PedidoCreateRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class PedidoRepository(BaseRepository[Pedido, PedidoCreateRequest, PedidoCreateRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Pedido, db_session)

    async def create_pedido(self, id_aocs: int, pedido_req: PedidoCreateRequest) -> Pedido:
        # Override or specific method to handle id_aocs injection
        try:
            data = pedido_req.model_dump()
            data['id_aocs'] = id_aocs
            data['status_entrega'] = "Pendente"
            data['quantidade_entregue'] = 0
            
            # id_item_contrato comes from pedido_req?
            # Schema has item_contrato_id? Model has id_item_contrato.
            # Convert if needed.
            if 'item_contrato_id' in data:
                data['id_item_contrato'] = data.pop('item_contrato_id')
            
            db_obj = Pedido(**data)
            self.db_session.add(db_obj)
            await self.db_session.commit()
            await self.db_session.refresh(db_obj)
            return db_obj
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro create pedido: {e}")
            raise e
