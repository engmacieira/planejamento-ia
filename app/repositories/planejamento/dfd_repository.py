from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import logging

from app.models.planejamento.dfd_model import DFD
from app.models.planejamento.item_dfd_model import ItemDFD
from app.models.planejamento.dfd_equipe_model import DFDEquipe
from app.models.planejamento.dfd_dotacao_model import DFDDotacao
from app.schemas.planejamento.dfd_schema import DFDCreate
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class DFDRepository(BaseRepository[DFD, DFDCreate, DFDCreate]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(DFD, db_session)

    async def create(self, dfd: DFDCreate) -> DFD:
        try:
            # 1. Separa os dados principais
            dfd_data = dfd.model_dump(exclude={"itens", "equipe", "dotacoes"})
            
            if 'id_unidade_requisitante' in dfd_data:
                dfd_data['unidade_requisitante_id'] = dfd_data.pop('id_unidade_requisitante')

            # Map legacy schema fields to new Model fields
            if 'objeto' in dfd_data:
                dfd_data['descricao_sucinta'] = dfd_data.pop('objeto')
            if 'justificativa' in dfd_data:
                dfd_data['justificativa_necessidade'] = dfd_data.pop('justificativa')
            
            # Clean up fields not in Model yet (prevent TypeError)
            keys_to_remove = ['data_req', 'responsavel_id', 'numero_protocolo_string', 'contratacao_vinculada', 'data_contratacao']
            for key in keys_to_remove:
                dfd_data.pop(key, None)

            # 2. Salva o DFD
            db_dfd = DFD(**dfd_data)
            self.db_session.add(db_dfd)
            await self.db_session.flush()
            
            # 3. Adiciona os Itens
            if dfd.itens:
                for item in dfd.itens:
                    db_item = ItemDFD(**item.model_dump(), dfd_id=db_dfd.id)
                    self.db_session.add(db_item)
                
            # 4. Adiciona a Equipe
            if dfd.equipe:
                for membro in dfd.equipe:
                    db_membro = DFDEquipe(**membro.model_dump(), dfd_id=db_dfd.id)
                    self.db_session.add(db_membro)
                
            # 5. Adiciona as Dotações
            if dfd.dotacoes:
                for dotacao in dfd.dotacoes:
                    db_dot = DFDDotacao(**dotacao.model_dump(), dfd_id=db_dfd.id)
                    self.db_session.add(db_dot)
            
            await self.db_session.commit()
            await self.db_session.refresh(db_dfd)
            return db_dfd
            
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro create DFD: {e}")
            raise e

    async def get_all(self, skip: int = 0, limit: int = 100):
        try:
            query = select(DFD).where(DFD.is_active == True).offset(skip).limit(limit)
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Erro get_all DFD: {e}")
            return []
    
    async def update(self, dfd_id: int, dfd_data: dict) -> DFD:
        try:
            db_dfd = await self.get(dfd_id)
            if not db_dfd or not db_dfd.is_active: return None
            
            itens_data = dfd_data.pop('itens', None)
            equipe_data = dfd_data.pop('equipe', None)
            dotacoes_data = dfd_data.pop('dotacoes', None)
            
            # Update Simple Fields
            for key, value in dfd_data.items():
                if hasattr(db_dfd, key):
                    setattr(db_dfd, key, value)
            
            # Need to reload collection relationships explicitly if they aren't loaded, or use specific logic
            # Async ORM collection handling (clear/append) works if relationship is loaded.
            # BaseRepository.get() might not load them eagerly.
            # Using selectinload in a specific query for update might be safer.
            
            # Re-fetch with relationships for Update
            query = select(DFD).options(
                selectinload(DFD.itens), 
                selectinload(DFD.equipe),
                selectinload(DFD.dotacoes)
            ).where(DFD.id == dfd_id)
            result = await self.db_session.execute(query)
            db_dfd_loaded = result.scalars().first()

            if itens_data is not None:
                # To clear async, we might need to delete manually or use collection mutators if loaded
                # db_dfd_loaded.itens = [] # This works if loaded
                # But safer to clear via proper logic or replacing collection
                
                # Removing old items
                # for item in db_dfd_loaded.itens: await self.db_session.delete(item)
                # db_dfd_loaded.itens.clear() # If loaded
                
                # Simplest Async update strategy for collections:
                # 1. Delete all existing linked items (or use collection management)
                # 2. Add new
                
                # Using collection replacement (SQLAlchemy handles delete-orphan if configured cascade)
                # Assuming cascade='all, delete-orphan' in Model.
                
                new_itens = []
                for item in itens_data:
                    clean_item = {k: v for k, v in item.items() if k in ['catalogo_item_id', 'quantidade', 'valor_unitario_estimado', 'complemento_descricao']}
                    new_itens.append(ItemDFD(**clean_item))
                db_dfd_loaded.itens = new_itens

            if dotacoes_data is not None:
                new_dots = []
                for dot in dotacoes_data:
                    clean_dot = {k: v for k, v in dot.items() if k in ['dotacao_id']}
                    new_dots.append(DFDDotacao(**clean_dot))
                db_dfd_loaded.dotacoes = new_dots

            if equipe_data is not None:
                new_equipe = []
                for eq in equipe_data:
                    clean_eq = {k: v for k, v in eq.items() if k in ['agente_id', 'papel']}
                    new_equipe.append(DFDEquipe(**clean_eq))
                db_dfd_loaded.equipe = new_equipe

            await self.db_session.commit()
            await self.db_session.refresh(db_dfd_loaded)
            return db_dfd_loaded
            
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro update DFD: {e}")
            raise e
        
    async def update_item_prices(self, itens_data: list):
        try:
            for item in itens_data:
                # Assuming item has id and fields
                result = await self.db_session.execute(select(ItemDFD).where(ItemDFD.id == item.id))
                db_item = result.scalars().first()
                if db_item:
                    db_item.valor_unitario_estimado = item.valor_unitario_estimado
            
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e
        
    async def get_by_id(self, dfd_id: int):
        # Override to eager load details
        query = select(DFD).options(
            selectinload(DFD.itens).selectinload(ItemDFD.catalogo_item),
            selectinload(DFD.dotacoes).selectinload(DFDDotacao.dotacao),
            selectinload(DFD.equipe).selectinload(DFDEquipe.agente)
        ).where(DFD.id == dfd_id, DFD.is_active == True)
        
        result = await self.db_session.execute(query)
        return result.scalars().first()
        
    async def delete(self, dfd_id: int):
        try:
            db_dfd = await self.get(dfd_id)
            if not db_dfd: return False
            
            if db_dfd.etp_id is not None:
                raise Exception("Não é possível excluir este DFD pois ele faz parte de um ETP. Desvincule-o primeiro.")
            
            db_dfd.is_active = False
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e
