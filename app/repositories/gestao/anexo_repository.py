from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.models.gestao.anexo_model import Anexo
from app.schemas.gestao.anexo_schema import AnexoCreate
from app.repositories.base_repository import BaseRepository
from app.repositories.gestao.tipo_documento_repository import TipoDocumentoRepository

logger = logging.getLogger(__name__)

class AnexoRepository(BaseRepository[Anexo, AnexoCreate, AnexoCreate]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Anexo, db_session)
        self.tipodocumento_repo = TipoDocumentoRepository(db_session)

    async def create(self, anexo_create_data: AnexoCreate) -> Anexo:
        """
        Cria anexo com lógica de chaves estrangeiras dinâmicas.
        """
        try:
            # We strictly map what fields exist in Model.
            # BaseRepository create just does Model(**data).
            # AnexoCreate has fields like tipo_entidade, id_entidade which might not be in Model directly
            # Model has id_contrato, id_aocs.
            # We need to map 'id_entidade' + 'tipo_entidade' -> 'id_contrato' or 'id_aocs'.

            data = anexo_create_data.model_dump()
            
            tipo_entidade = data.pop('tipo_entidade', None)
            id_entidade = data.pop('id_entidade', None)
            
            if tipo_entidade == 'contrato':
                data['id_contrato'] = id_entidade
                data['tipo_entidade'] = 'contrato' # If model has this field
            elif tipo_entidade == 'aocs':
                data['id_aocs'] = id_entidade
                data['tipo_entidade'] = 'aocs'
            else:
                 # If we allow other types or fallback
                 if tipo_entidade: data['tipo_entidade'] = tipo_entidade
            
            # Remove any fields not in model if present
            # Assumption: Anexo model matches SQL columns used in original repo:
            # nome_original, nome_seguro, data_upload, tipo_documento, tipo_entidade, id_contrato, id_aocs
            
            db_obj = Anexo(**data)
            self.db_session.add(db_obj)
            await self.db_session.commit()
            await self.db_session.refresh(db_obj)
            
            logger.info(f"Anexo ID {db_obj.id} ('{db_obj.nome_original}') criado.")
            return db_obj

        except Exception as error:
            await self.db_session.rollback()
            logger.exception(f"Erro inesperado ao criar registro de anexo (Data: {anexo_create_data}): {error}")
            raise

    async def get_by_entidade(self, id_entidade: int, tipo_entidade: str) -> list[Anexo]:
        try:
            query = select(Anexo).where(Anexo.tipo_entidade == tipo_entidade)
            
            if tipo_entidade == 'contrato':
                query = query.where(Anexo.id_contrato == id_entidade)
            elif tipo_entidade == 'aocs':
                query = query.where(Anexo.id_aocs == id_entidade)
            
            query = query.order_by(Anexo.data_upload.desc())
            
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as error:
             logger.exception(f"Erro ao buscar anexos ({tipo_entidade}={id_entidade}): {error}")
             return []
