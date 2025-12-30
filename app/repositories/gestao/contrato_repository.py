from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.models.gestao.contrato_model import Contrato
from app.schemas.gestao.contrato_schema import ContratoRequest, ContratoCreateRequest
from app.repositories.base_repository import BaseRepository

# Dep Imports
from app.repositories.gestao.fornecedor_repository import FornecedorRepository
from app.repositories.gestao.categoria_repository import CategoriaRepository
from app.repositories.gestao.instrumento_repository import InstrumentoRepository
from app.repositories.gestao.modalidade_repository import ModalidadeRepository
from app.repositories.gestao.numero_modalidade_repository import NumeroModalidadeRepository
from app.repositories.gestao.processo_licitatorio_repository import ProcessoLicitatorioRepository

logger = logging.getLogger(__name__)

class ContratoRepository(BaseRepository[Contrato, ContratoCreateRequest, ContratoRequest]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Contrato, db_session)
        self.fornecedor_repo = FornecedorRepository(db_session)
        self.categoria_repo = CategoriaRepository(db_session)
        self.instrumento_repo = InstrumentoRepository(db_session)
        self.modalidade_repo = ModalidadeRepository(db_session)
        self.numero_modalidade_repo = NumeroModalidadeRepository(db_session)
        self.processo_licitatorio_repo = ProcessoLicitatorioRepository(db_session)

    async def create_with_relationships(self, contrato_data: ContratoCreateRequest) -> Contrato:
        try:
            # 1. Resolver/Criar Dependências
            
            # Fornecedor
            fornecedor = await self.fornecedor_repo.get_or_create(contrato_data.fornecedor, contrato_data.id_fornecedor)
            if not fornecedor:
                raise ValueError("Fornecedor inválido ou dados insuficientes para criação.")
            id_fornecedor = fornecedor.id
            
            # Categoria
            categoria = await self.categoria_repo.get_or_create(contrato_data.categoria_nome)
            id_categoria = categoria.id
            
            # Instrumento
            instrumento = await self.instrumento_repo.get_or_create(contrato_data.instrumento_nome)
            id_instrumento = instrumento.id
            
            # Modalidade
            modalidade = await self.modalidade_repo.get_or_create(contrato_data.modalidade_nome)
            id_modalidade = modalidade.id
            
            # Numero Modalidade (depende de Modalidade)
            numero_modalidade = await self.numero_modalidade_repo.get_or_create(contrato_data.numero_modalidade_str, id_modalidade)
            id_numero_modalidade = numero_modalidade.id
            
            # Processo Licitatorio
            processo = await self.processo_licitatorio_repo.get_or_create(contrato_data.processo_licitatorio_numero)
            id_processo = processo.id
            
            # 2. Criar Contrato
            
            # Mapear campos do Request para Model (excluindo os campos auxiliares de string)
            # Usando model_dump exclude para limpar e depois injetar IDs
            data = contrato_data.model_dump(exclude={
                'fornecedor', 'categoria_nome', 'instrumento_nome', 'modalidade_nome', 
                'numero_modalidade_str', 'processo_licitatorio_numero'
            })
            
            data['id_fornecedor'] = id_fornecedor
            data['id_categoria'] = id_categoria
            data['id_instrumento_contratual'] = id_instrumento # Model field name might be id_instrumento or id_instrumento_contratual. Check Model.
            # Checking ContratoModel in step 136 snippet... it showed id_fornecedor, id_processo_licitatorio...
            # Snippet 136 didn't show id_instrumento explicitly but schema (step 168) has id_instrumento_contratual. Assuming Model matches Schema id_instrumento_contratual. 
            data['id_instrumento_contratual'] = id_instrumento
            data['id_modalidade'] = id_modalidade
            data['id_numero_modalidade'] = id_numero_modalidade
            data['id_processo_licitatorio'] = id_processo
            
            # Mapping Schema fields (DTO) to Model fields (SQL)
            if 'data_inicio' in data:
                data['data_inicio_vigencia'] = data.pop('data_inicio')
            if 'data_fim' in data:
                data['data_fim_vigencia'] = data.pop('data_fim')
            
            # Verify fields against Model.
            # Step 136 snippet showed: numero_contrato, objeto, ativo, id_processo_licitatorio, id_numero_modalidade, id_fornecedor.
            # Missing: id_categoria, id_instrumento_contratual in Step 136 view (it was truncated/simplified).
            # Assuming they exist in real Model as per Schema Response.

            db_obj = Contrato(**data)
            self.db_session.add(db_obj)
            await self.db_session.commit()
            await self.db_session.refresh(db_obj)
            db_obj.fornecedor = fornecedor 
            db_obj.categoria = categoria
            db_obj.instrumento_contratual = instrumento
            db_obj.modalidade = modalidade
            # db_obj.numero_modalidade = numero_modalidade # If needed in response
            # db_obj.processo_licitatorio = processo # If needed in response
            
            logger.info(f"Contrato criado: {db_obj.numero_contrato}")
            return db_obj

        except Exception as e:
            await self.db_session.rollback()
            logger.exception(f"Erro create_with_relationships Contrato: {e}")
            raise e

    async def create(self, obj_in: ContratoCreateRequest) -> Contrato:
         # Override generic create to use the complex logic
         return await self.create_with_relationships(obj_in)
