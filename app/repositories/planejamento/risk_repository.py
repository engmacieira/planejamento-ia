from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import logging

from app.models.planejamento.matriz_risco_model import MatrizRisco
from app.models.planejamento.item_risco_model import ItemRisco

logger = logging.getLogger(__name__)

class RiskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def get_by_etp(self, etp_id: int):
        """Busca a matriz de risco de um ETP (cria se não existir)."""
        try:
            # Check existing
            query = select(MatrizRisco).options(selectinload(MatrizRisco.riscos)).where(MatrizRisco.etp_id == etp_id)
            result = await self.db_session.execute(query)
            matriz = result.scalars().first()
            
            if not matriz:
                # Cria automaticamente se não existir
                matriz = MatrizRisco(etp_id=etp_id)
                self.db_session.add(matriz)
                await self.db_session.commit()
                await self.db_session.refresh(matriz)
                # Need to reload to ensure relationships if accessed? Empty for new.
            
            return matriz
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro get_by_etp risk: {e}")
            raise e

    async def add_risk(self, matriz_id: int, risk_data: dict):
        """Adiciona um novo risco à matriz."""
        try:
            risco = ItemRisco(matriz_id=matriz_id, **risk_data)
            self.db_session.add(risco)
            await self.db_session.commit()
            await self.db_session.refresh(risco)
            return risco
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro add_risk: {e}")
            raise e

    async def delete_risk(self, risk_id: int):
        """Remove um risco."""
        try:
            query = select(ItemRisco).where(ItemRisco.id == risk_id)
            result = await self.db_session.execute(query)
            risco = result.scalars().first()
            if risco:
                await self.db_session.delete(risco)
                await self.db_session.commit()
                return True
            return False
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro delete_risk: {e}")
            raise e
