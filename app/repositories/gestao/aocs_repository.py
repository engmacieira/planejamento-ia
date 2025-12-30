from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
import logging

from app.models.gestao.aocs_model import Aocs
from app.schemas.gestao.aocs_schema import AocsCreateRequest, AocsUpdateRequest
from app.repositories.base_repository import BaseRepository
from app.repositories.core.unidade_repository import UnidadeRepository
from app.repositories.gestao.local_repository import LocalRepository
from app.repositories.core.agente_repository import AgenteRepository
from app.repositories.gestao.dotacao_repository import DotacaoRepository

logger = logging.getLogger(__name__)

class AocsRepository(BaseRepository[Aocs, AocsCreateRequest, AocsUpdateRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Aocs, db_session)
        self.unidade_repo = UnidadeRepository(db_session)
        self.local_repo = LocalRepository(db_session)
        self.agente_repo = AgenteRepository(db_session)
        self.dotacao_repo = DotacaoRepository(db_session)

    async def create(self, aocs_req: AocsCreateRequest) -> Aocs:
        try:
            # Resolve text fields to IDs if necessary
            
            # Unidade
            if isinstance(aocs_req.unidade_requisitante, str):
                unidade = await self.unidade_repo.get_or_create(aocs_req.unidade_requisitante)
                id_unidade = unidade.id
            else:
                id_unidade = aocs_req.unidade_requisitante

            # Local
            if isinstance(aocs_req.local_entrega, str):
                local = await self.local_repo.get_or_create(aocs_req.local_entrega)
                id_local = local.id
            else:
                id_local = aocs_req.local_entrega

            # Agente
            if isinstance(aocs_req.agente_responsavel, str):
                agente = await self.agente_repo.get_or_create(aocs_req.agente_responsavel)
                id_agente = agente.id
            else:
                id_agente = aocs_req.agente_responsavel
            
            # Dotação
            if isinstance(aocs_req.dotacao_orcamentaria, str):
                dotacao = await self.dotacao_repo.get_or_create(aocs_req.dotacao_orcamentaria)
                id_dotacao = dotacao.id
            else:
                id_dotacao = aocs_req.dotacao_orcamentaria

            # Construct default data (assuming IDs are set correctly now)
            # Create a dict from schema, replace raw fields with resolved IDs
            data = aocs_req.model_dump()
            data['id_unidade_requisitante'] = id_unidade
            data['id_local_entrega'] = id_local
            data['id_agente_responsavel'] = id_agente
            data['id_dotacao_orcamentaria'] = id_dotacao
            
            # Remove keys that might conflict if schema uses names instead of 'id_...' key (e.g. if schema has 'unidade_requisitante' but model has 'id_unidade_requisitante')
            # Assuming Schema maps to JSON fields which might be strings.
            # We overwrite them or ensure Model accepts them.
            # Model usually uses 'id_...' for FKs.
            # The schema keys: 'unidade_requisitante' -> Model 'id_unidade_requisitante'
            # We must cleanup the dict to match Model constraints.
            
            data.pop('unidade_requisitante', None)
            data.pop('local_entrega', None)
            data.pop('agente_responsavel', None)
            data.pop('dotacao_orcamentaria', None)
            
            if not data.get('data_criacao'):
                 data['data_criacao'] = date.today()

            db_obj = Aocs(**data)
            self.db_session.add(db_obj)
            await self.db_session.commit()
            await self.db_session.refresh(db_obj)

            logger.info(f"Aocs criada com ID {db_obj.id}: {db_obj.numero_aocs}")
            return db_obj

        except Exception as error:
            await self.db_session.rollback()
            logger.exception(f"Erro inesperado ao criar Aocs (Req: {aocs_req}): {error}")
            raise
