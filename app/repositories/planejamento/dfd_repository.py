from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload
import logging

from app.models.planejamento.dfd_model import DFD
from app.models.planejamento.item_dfd_model import ItemDFD
from app.models.planejamento.dfd_equipe_model import DFDEquipe
from app.models.planejamento.dfd_dotacao_model import DFDDotacao
from app.models.core.unidade_model import Unidade
from app.schemas.planejamento.dfd_schema import DFDCreate
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class DFDRepository(BaseRepository[DFD, DFDCreate, DFDCreate]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(DFD, db_session)

    async def _get_proximo_numero(self, ano: int) -> int:
        stmt = select(func.max(DFD.numero)).where(DFD.ano == ano)
        result = await self.db_session.execute(stmt)
        max_numero = result.scalar()
        return (max_numero or 0) + 1

    async def create(self, dfd: DFDCreate) -> DFD:
        try:
            # 1. Preparação dos dados do Pai (DFD)
            dfd_data = dfd.model_dump(exclude={"itens", "equipe", "dotacoes"})
            
            # Mapeamentos seguros
            if 'id_unidade_requisitante' in dfd_data:
                dfd_data['unidade_requisitante_id'] = dfd_data.pop('id_unidade_requisitante')
            if 'objeto' in dfd_data:
                dfd_data['descricao_sucinta'] = dfd_data.pop('objeto')
            if 'justificativa' in dfd_data:
                dfd_data['justificativa_necessidade'] = dfd_data.pop('justificativa')
            
            # Limpeza de campos que não existem no Model
            keys_to_remove = ['numero_protocolo_string', 'contratacao_vinculada', 'data_contratacao']
            for key in keys_to_remove:
                dfd_data.pop(key, None)

            # Autoincremento
            if 'numero' not in dfd_data or dfd_data['numero'] is None:
                ano_ref = dfd_data.get('ano')
                if not ano_ref:
                    raise ValueError("Ano obrigatório para gerar número.")
                dfd_data['numero'] = await self._get_proximo_numero(ano_ref)

            # 2. Salva Pai
            db_dfd = DFD(**dfd_data)
            self.db_session.add(db_dfd)
            await self.db_session.flush() # Gera o ID
            
            # 3. Salva Itens (Com Filtragem Explícita)
            if dfd.itens:
                for i, item in enumerate(dfd.itens, start=1):
                    raw_item = item.model_dump()
                    
                    # Criação limpa: só passamos o que o model aceita
                    clean_item = {
                        'dfd_id': db_dfd.id,
                        'numero_item': i,
                        'quantidade': raw_item.get('quantidade'),
                        'valor_unitario_estimado': raw_item.get('valor_unitario_estimado'),
                        'complemento_descricao': raw_item.get('complemento_descricao')
                    }
                    
                    # Resolve o ID do catálogo (aceita ambos os nomes)
                    if 'catalogo_item_id' in raw_item:
                        clean_item['catalogo_item_id'] = raw_item['catalogo_item_id']
                    elif 'id_catalogo_item' in raw_item:
                        clean_item['catalogo_item_id'] = raw_item['id_catalogo_item']
                    
                    db_item = ItemDFD(**clean_item)
                    self.db_session.add(db_item)
                
            # 4. Salva Equipe
            if dfd.equipe:
                for membro in dfd.equipe:
                    # Pode aplicar a mesma lógica de limpeza aqui se der erro em Equipe
                    db_membro = DFDEquipe(**membro.model_dump(), dfd_id=db_dfd.id)
                    self.db_session.add(db_membro)
                
            # 5. Salva Dotações
            if dfd.dotacoes:
                for dotacao in dfd.dotacoes:
                    db_dot = DFDDotacao(**dotacao.model_dump(), dfd_id=db_dfd.id)
                    self.db_session.add(db_dot)
            
            await self.db_session.commit()
            
            # Retorna objeto recarregado com relacionamentos para o Pydantic não reclamar
            return await self.get_by_id(db_dfd.id)
            
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro create DFD: {e}")
            raise e

    async def get_all(self, skip: int = 0, limit: int = 100):
        query = select(DFD).options(
            selectinload(DFD.unidade_requisitante)
        ).where(DFD.is_active == True).offset(skip).limit(limit)
        
        result = await self.db_session.execute(query)
        return result.scalars().all()
    
    async def update(self, dfd_id: int, dfd_data: dict) -> DFD:
        try:
            db_dfd = await self.get_by_id(dfd_id)
            if not db_dfd: return None
            
            itens_data = dfd_data.pop('itens', None)
            equipe_data = dfd_data.pop('equipe', None)
            dotacoes_data = dfd_data.pop('dotacoes', None)
            
            for key, value in dfd_data.items():
                if hasattr(db_dfd, key):
                    setattr(db_dfd, key, value)
            
            # Atualização de Itens (Recriação Limpa)
            if itens_data is not None:
                db_dfd.itens = [] 
                for i, item in enumerate(itens_data, start=1):
                    # Lógica de limpeza idêntica ao create
                    clean_item = {
                        'numero_item': i,
                        'quantidade': item.get('quantidade'),
                        'valor_unitario_estimado': item.get('valor_unitario_estimado'),
                        'complemento_descricao': item.get('complemento_descricao')
                    }
                    if 'catalogo_item_id' in item:
                        clean_item['catalogo_item_id'] = item['catalogo_item_id']
                    elif 'id_catalogo_item' in item:
                        clean_item['catalogo_item_id'] = item['id_catalogo_item']

                    db_dfd.itens.append(ItemDFD(**clean_item))

            if dotacoes_data is not None:
                db_dfd.dotacoes = []
                for dot in dotacoes_data:
                    clean = {k: v for k, v in dot.items() if k in ['dotacao_id']}
                    db_dfd.dotacoes.append(DFDDotacao(**clean))

            if equipe_data is not None:
                db_dfd.equipe = []
                for eq in equipe_data:
                    clean = {k: v for k, v in eq.items() if k in ['agente_id', 'papel']}
                    db_dfd.equipe.append(DFDEquipe(**clean))

            await self.db_session.commit()
            return await self.get_by_id(dfd_id)
            
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro update DFD: {e}")
            raise e
        
    async def update_item_prices(self, itens_data: list):
        try:
            for item in itens_data:
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
        query = select(DFD).options(
            selectinload(DFD.itens).selectinload(ItemDFD.catalogo_item),
            selectinload(DFD.dotacoes).selectinload(DFDDotacao.dotacao),
            selectinload(DFD.equipe).selectinload(DFDEquipe.agente),
            selectinload(DFD.unidade_requisitante)
        ).where(DFD.id == dfd_id, DFD.is_active == True)
        
        result = await self.db_session.execute(query)
        return result.scalars().first()
        
    async def delete(self, dfd_id: int):
        try:
            db_dfd = await self.get_by_id(dfd_id)
            if not db_dfd: return False
            if db_dfd.etp_id is not None:
                raise Exception("Vinculado a ETP")
            db_dfd.is_active = False
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e