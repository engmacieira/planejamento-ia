import pytest
from app.repositories.gestao.dotacao_repository import DotacaoRepository
from app.schemas.gestao.dotacao_schema import DotacaoRequest

@pytest.mark.asyncio
async def test_dotacao_crud_logic(db_session):
    repo = DotacaoRepository(db_session)
    
    # Test Create
    d_in = DotacaoRequest(descricao="Dotação Teste 2024")
    dotacao = await repo.create(d_in)
    assert dotacao.id is not None
    assert dotacao.descricao == "Dotação Teste 2024"
    
    # Test Get By Descricao
    fetched = await repo.get_by_descricao("Dotação Teste 2024")
    assert fetched.id == dotacao.id
    
    # Test Get Or Create (Existing)
    goc_existing = await repo.get_or_create("Dotação Teste 2024")
    assert goc_existing.id == dotacao.id
    
    # Test Get Or Create (New)
    goc_new = await repo.get_or_create("Dotação Nova")
    assert goc_new.id is not None
    assert goc_new.id != dotacao.id
    assert goc_new.descricao == "Dotação Nova"
