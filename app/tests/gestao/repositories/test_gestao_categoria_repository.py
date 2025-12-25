import pytest
from app.repositories.gestao.categoria_repository import CategoriaRepository
from app.schemas.gestao.categoria_schema import CategoriaRequest

@pytest.mark.asyncio
async def test_categoria_crud(db_session):
    repo = CategoriaRepository(db_session)
    
    # Create
    cat_in = CategoriaRequest(nome="Nova Categoria Teste", codigo_taxonomia="NCT")
    cat = await repo.create(cat_in)
    assert cat.id is not None
    assert cat.nome == "Nova Categoria Teste"
    
    # Get by Nome
    cat_fetched = await repo.get_by_nome("Nova Categoria Teste")
    assert cat_fetched is not None
    assert cat_fetched.id == cat.id
    
    # Get Or Create (Existing)
    cat_goc = await repo.get_or_create("Nova Categoria Teste")
    assert cat_goc.id == cat.id
    
    # Get Or Create (New)
    cat_new = await repo.get_or_create("Outra Categoria")
    assert cat_new.id is not None
    assert cat_new.nome == "Outra Categoria"
    assert cat_new.id != cat.id
