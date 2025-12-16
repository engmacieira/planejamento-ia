from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.models.planejamento.tr_model import TR
from app.models.planejamento.matriz_risco_model import MatrizRisco

logger = logging.getLogger(__name__)

class TRRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def get_by_etp(self, etp_id: int):
        """
        Busca o TR vinculado ao ETP via MatrizRisco.
        """
        try:
            # 1. Acha a Matriz do ETP
            result = await self.db_session.execute(select(MatrizRisco).where(MatrizRisco.etp_id == etp_id))
            matriz = result.scalars().first()
            if not matriz:
                return None 

            # 2. Acha o TR vinculado à Matriz
            result_tr = await self.db_session.execute(select(TR).where(TR.matriz_id == matriz.id))
            tr = result_tr.scalars().first()
            
            # 3. Se não existe, cria o rascunho inicial
            if not tr:
                tr = TR(matriz_id=matriz.id)
                self.db_session.add(tr)
                await self.db_session.commit()
                await self.db_session.refresh(tr)
            
            return tr
        except Exception as e:
             await self.db_session.rollback()
             logger.error(f"Erro get_by_etp TR: {e}")
             raise e

    async def update(self, tr_id: int, tr_data: dict):
        try:
            # Reusing Generic Update logic would be better if Inheriting BaseRepo, but tr_data is dict here.
            # Using specific logic for now.
            query = select(TR).where(TR.id == tr_id)
            result = await self.db_session.execute(query)
            db_tr = result.scalars().first()
            
            if not db_tr: return None
            
            for key, value in tr_data.items():
                if hasattr(db_tr, key):
                    setattr(db_tr, key, value)
            
            await self.db_session.commit()
            await self.db_session.refresh(db_tr)
            return db_tr
        except Exception as e:
            await self.db_session.rollback()
            raise e
