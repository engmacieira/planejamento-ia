from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
import logging

from app.models.gestao.fornecedor_model import Fornecedor
from app.schemas.gestao.fornecedor_schema import FornecedorRequest
from app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)

class FornecedorRepository(BaseRepository[Fornecedor, FornecedorRequest, FornecedorRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Fornecedor, db_session)

    async def get_by_cpf_cnpj(self, cpf_cnpj: str) -> Fornecedor | None:
        try:
            query = select(Fornecedor).where(Fornecedor.cpf_cnpj == cpf_cnpj)
            result = await self.db_session.execute(query)
            return result.scalars().first()
        except Exception as e:
             logger.exception(f"Erro ao buscar fornecedor por CPF/CNPJ '{cpf_cnpj}': {e}")
             return None

    async def get_or_create(self, fornecedor_data: FornecedorRequest | None, id_fornecedor: int | None = None) -> Fornecedor | None:
        """
        Tenta buscar por ID (se fornecido) ou CPF/CNPJ (se dados fornecidos).
        Se não encontrar e houver dados, cria.
        """
        try:
            if id_fornecedor:
                fornecedor = await self.get_by_id(id_fornecedor)
                if fornecedor: return fornecedor
            
            if fornecedor_data and fornecedor_data.cpf_cnpj:
                fornecedor = await self.get_by_cpf_cnpj(fornecedor_data.cpf_cnpj)
                if fornecedor: return fornecedor
                
                # Create
                return await self.create(fornecedor_data)
                
            return None
        except Exception as e:
             logger.error(f"Erro get_or_create Fornecedor: {e}")
             raise e
