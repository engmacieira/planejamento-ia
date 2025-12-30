from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.core.unidade_model import Unidade
from app.models.core.agente_model import Agente
from app.models.gestao.catalogo_item_model import CatalogoItem
from app.models.gestao.dotacao_model import Dotacao

class CadastroRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    # --- Unidades (Antigas Secretarias) ---
    async def get_all_unidades(self):
        result = await self.db_session.execute(select(Unidade).where(Unidade.ativo == True))
        return result.scalars().all()

    # --- Agentes ---
    async def get_all_agentes(self):
        result = await self.db_session.execute(select(Agente).where(Agente.is_active == True))
        return result.scalars().all()

    # --- Itens do Catálogo (Nova Estrutura) ---
    async def get_all_itens(self):
        result = await self.db_session.execute(select(CatalogoItem).where(CatalogoItem.is_active == True))
        itens = result.scalars().all()
        
        resultado = []
        for i in itens:
            resultado.append({
                "id": i.id,
                "nome": i.nome_item, # Mapeia nome_item -> nome
                "unidade_medida": i.unidade_medida,
                "codigo": i.codigo_identificacao_completo,
                "descricao": i.descricao_detalhada,
                "tipo": i.tipo,
                "is_active": i.is_active
            })
        return resultado

    # --- Dotações ---
    async def get_all_dotacoes(self):
        result = await self.db_session.execute(select(Dotacao).where(Dotacao.is_active == True))
        return result.scalars().all()
