from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from fastapi import HTTPException
import logging

from app.models.planejamento.etp_model import ETP
from app.models.planejamento.dfd_model import DFD
from app.models.planejamento.item_etp_model import ItemETP
from app.models.planejamento.etp_equipe_model import ETPEquipe
from app.models.planejamento.etp_dotacao_model import ETPDotacao
from app.models.planejamento.item_dfd_model import ItemDFD
from app.schemas.planejamento.etp_schema import ETPCreate
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class ETPRepository(BaseRepository[ETP, ETPCreate, ETPCreate]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ETP, db_session)
    
    async def _get_etp_query(self):
        """Query base que já carrega os relacionamentos necessários (Eager Loading)"""
        return select(ETP).options(
            selectinload(ETP.itens).selectinload(ItemETP.catalogo_item),
            selectinload(ETP.equipe).selectinload(ETPEquipe.agente),
            selectinload(ETP.dotacoes).selectinload(ETPDotacao.dotacao)
        )

    async def get_by_id(self, etp_id: int) -> ETP | None:
        try:
             query = (await self._get_etp_query()).where(ETP.id == etp_id, ETP.is_active == True)
             result = await self.db_session.execute(query)
             return result.scalars().first()
        except Exception as e:
             logger.error(f"Erro get_by_id ETP: {e}")
             return None

    async def get_by_dfd(self, dfd_id: int) -> ETP | None:
        """Busca o ETP através de um dos DFDs vinculados."""
        try:
            result_dfd = await self.db_session.execute(select(DFD).where(DFD.id == dfd_id))
            dfd = result_dfd.scalars().first()
            if dfd and dfd.etp_id:
                return await self.get_by_id(dfd.etp_id)
            return None
        except Exception as e:
            logger.error(f"Erro get_by_dfd ETP: {e}")
            return None

    async def consolidar_dfds(self, dfd_ids: list[int]) -> ETP:
        """
        Cria um ETP consolidando múltiplos DFDs.
        """
        try:
            # 1. Validar DFDs (com itens carregados)
            query = select(DFD).options(selectinload(DFD.itens)).where(DFD.id.in_(dfd_ids))
            result = await self.db_session.execute(query)
            dfds = result.scalars().all()
            
            if len(dfds) != len(dfd_ids):
                raise HTTPException(status_code=404, detail="Um ou mais DFDs não foram encontrados.")
                
            for dfd in dfds:
                if dfd.etp_id is not None:
                    raise HTTPException(status_code=400, detail=f"O DFD {dfd.numero} já pertence a um ETP.")
                
            # 2. Criar ETP
            novo_etp = ETP(
                descricao_necessidade="ETP Consolidado - Aguardando geração de texto...",
                viabilidade=False
            )
            self.db_session.add(novo_etp)
            await self.db_session.flush() 

            # 3. Vincular DFDs
            for dfd in dfds:
                dfd.etp_id = novo_etp.id
                dfd.status = "Em ETP"
            
            # 4. CONSOLIDAR ITENS (Soma)
            itens_map = {} # { catalogo_item_id: quantidade_total }
            
            for dfd in dfds:
                for item_dfd in dfd.itens:
                    cat_id = item_dfd.catalogo_item_id
                    qtd = float(item_dfd.quantidade)
                    
                    if cat_id in itens_map:
                        itens_map[cat_id] += qtd
                    else:
                        itens_map[cat_id] = qtd
            
            if not itens_map:
                logger.warning("Nenhum item encontrado nos DFDs para consolidar.")

            for cat_id, qtd_total in itens_map.items():
                item_etp = ItemETP(
                    etp_id=novo_etp.id,
                    catalogo_item_id=cat_id,
                    quantidade_total=qtd_total,
                    valor_unitario_referencia=0.0,
                    valor_total_estimado=0.0
                )
                self.db_session.add(item_etp)

            # 5. Consolidar Equipe e Dotações (Omitido/Simplificado - add logic if needed)

            await self.db_session.commit()
            
            # Retorna o objeto completo recarregado do banco
            return await self.get_by_id(novo_etp.id)

        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro consolidar_dfds: {e}")
            raise e

    async def update(self, etp_id: int, etp_data: dict) -> ETP:
        try:
             db_etp = await self.get(etp_id)
             if not db_etp: return None
             
             for key, value in etp_data.items():
                 if hasattr(db_etp, key):
                     setattr(db_etp, key, value)
            
             await self.db_session.commit()
             await self.db_session.refresh(db_etp)
             return db_etp
        except Exception as e:
             await self.db_session.rollback()
             raise e

    async def update_item_prices(self, itens_data: list):
        try:
            for item in itens_data:
                result = await self.db_session.execute(select(ItemETP).where(ItemETP.id == item.id))
                db_item = result.scalars().first()
                if db_item:
                    db_item.valor_unitario_referencia = item.valor_unitario_referencia
                    db_item.valor_total_estimado = float(db_item.quantidade_total) * item.valor_unitario_referencia
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e
        
    async def unlink_dfd(self, etp_id: int, dfd_id: int):
        """Remove o vínculo de um DFD com o ETP, devolvendo-o para o status de Rascunho."""
        try:
            result = await self.db_session.execute(select(DFD).where(DFD.id == dfd_id, DFD.etp_id == etp_id))
            dfd = result.scalars().first()
            if not dfd:
                raise Exception("DFD não encontrado neste ETP.")
                
            dfd.etp_id = None
            dfd.status = "Rascunho"
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def delete(self, etp_id: int):
        """Soft Delete do ETP. Libera todos os DFDs vinculados."""
        try:
            # Load with DFDs
            result = await self.db_session.execute(select(ETP).options(selectinload(ETP.dfds)).where(ETP.id == etp_id))
            etp = result.scalars().first()
            if not etp: return False
            
            # Libera os DFDs presos a este ETP
            for dfd in etp.dfds:
                dfd.etp_id = None
                dfd.status = "Rascunho"
                
            etp.is_active = False
            await self.db_session.commit()
            return True
        except Exception as e:
            await self.db_session.rollback()
            raise e
