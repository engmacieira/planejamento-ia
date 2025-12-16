from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.planejamento.numero_modalidade_model import NumeroModalidade
from app.schemas.gestao.numero_modalidade_schema import NumeroModalidadeRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class NumeroModalidadeRepository(BaseRepository[NumeroModalidade, NumeroModalidadeRequest, NumeroModalidadeRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(NumeroModalidade, db_session)

    async def get_by_numero_ano_modalidade(self, numero: int, ano: int, id_modalidade: int) -> NumeroModalidade | None:
        try:
            query = select(NumeroModalidade).where(
                NumeroModalidade.numero == numero,
                NumeroModalidade.ano == ano,
                NumeroModalidade.id_modalidade == id_modalidade
            )
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
             logger.exception(f"Erro ao buscar numero_modalidade {numero}/{ano} (Mod: {id_modalidade}): {e}")
             return None

    async def get_or_create(self, numero_ano: str, id_modalidade: int) -> NumeroModalidade:
        try:
            parts = numero_ano.split('/')
            if len(parts) != 2:
                raise ValueError(f"Formato inválido numero_ano: {numero_ano}. Esperado 'NUMERO/ANO'.")
            
            numero = int(parts[0])
            ano = int(parts[1])

            obj = await self.get_by_numero_ano_modalidade(numero, ano, id_modalidade)
            if obj:
                return obj
            
            # Create
            try:
                # We can't use generic create easily because schema doesn't fit model fields directly (schema has string, model has ints)
                # So we manually instantiate
                new_obj = NumeroModalidade(numero=numero, ano=ano, id_modalidade=id_modalidade)
                self.db_session.add(new_obj)
                await self.db_session.commit()
                await self.db_session.refresh(new_obj)
                return new_obj
            except IntegrityError:
                await self.db_session.rollback()
                obj = await self.get_by_numero_ano_modalidade(numero, ano, id_modalidade)
                if obj: return obj
                raise

        except Exception as e:
             logger.error(f"Erro em get_or_create NumeroModalidade '{numero_ano}' (Mod: {id_modalidade}): {e}")
             raise e
