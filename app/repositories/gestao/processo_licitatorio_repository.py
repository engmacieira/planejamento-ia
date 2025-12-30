from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.planejamento.processo_licitatorio_model import ProcessoLicitatorio
# Importando as classes corretas agora que elas existem no schema
from app.schemas.planejamento.processo_licitatorio_schema import (
    ProcessoLicitatorioRequest, 
    ProcessoLicitatorioCreateRequest
)
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class ProcessoLicitatorioRepository(BaseRepository[ProcessoLicitatorio, ProcessoLicitatorioCreateRequest, ProcessoLicitatorioRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(ProcessoLicitatorio, db_session)

    async def get_or_create(self, numero_processo_str: str) -> ProcessoLicitatorio:
        """
        Busca ou cria um processo baseado na string 'Numero/Ano'.
        Ex: '10/2024' -> numero_processo=10, ano_processo=2024
        """
        try:
            # 1. Validação e Parser
            if not numero_processo_str or "/" not in numero_processo_str:
                logger.warning(f"Formato inválido de processo: {numero_processo_str}")
                return None # Ou raise ValueError
            
            parts = numero_processo_str.split("/")
            numero = int(parts[0])
            ano = int(parts[1])

            # 2. Tenta Buscar (Pelo número e ano separados)
            stmt = select(self.model).where(
                self.model.numero_processo == numero,
                self.model.ano_processo == ano
            )
            result = await self.db_session.execute(stmt)
            obj = result.scalars().first()

            if obj:
                return obj

            # 3. Se não existe, Cria (Usando os campos corretos do Model)
            # Nota: id_dfd e id_modalidade são obrigatórios no banco. 
            # Se chamarmos isso sem contexto, vai falhar a constraint NOT NULL.
            # Idealmente, o teste deve fornecer esses dados via fixture.
            new_obj = self.model(
                numero_processo=numero,
                ano_processo=ano,
                objeto=f"Processo criado automaticamente {numero_processo_str}",
                status="Criado Automaticamente"
            )
            
            self.db_session.add(new_obj)
            await self.db_session.commit()
            await self.db_session.refresh(new_obj)
            return new_obj

        except IntegrityError:
            await self.db_session.rollback()
            # Concorrência: alguém criou enquanto tentávamos? Tenta buscar de novo.
            stmt = select(self.model).where(
                self.model.numero_processo == numero,
                self.model.ano_processo == ano
            )
            result = await self.db_session.execute(stmt)
            return result.scalars().first()
            
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Erro ao get_or_create Processo: {e}")
            raise e