from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.models.gestao.ci_pagamento_model import CiPagamento
from app.schemas.gestao.ci_pagamento_schema import CiPagamentoCreateRequest
from app.repositories.base_repository import BaseRepository
from app.repositories.core.unidade_repository import UnidadeRepository
from app.repositories.gestao.aocs_repository import AocsRepository

logger = logging.getLogger(__name__)

class CiPagamentoRepository(BaseRepository[CiPagamento, CiPagamentoCreateRequest, CiPagamentoCreateRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(CiPagamento, db_session)
        self.unidade_repo = UnidadeRepository(db_session)
        self.aocs_repo = AocsRepository(db_session)

    async def create(self, ci_req: CiPagamentoCreateRequest) -> CiPagamento:
        try:
            # Assumes ci_req contains IDs. If manual resolution needed, add here.
            # Assuming generic create is sufficient if Schema fields match Model fields or are strictly mapped.
            # CiPagamentoCreateRequest -> CiPagamento
            # Check fields used in original sql: numero_ci, id_aocs, id_unidade, data_emissao
            
            db_obj = CiPagamento(**ci_req.model_dump())
            self.db_session.add(db_obj)
            await self.db_session.commit()
            await self.db_session.refresh(db_obj)
            return db_obj
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro create CI: {e}")
            raise e
