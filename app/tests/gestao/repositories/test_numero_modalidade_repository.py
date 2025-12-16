import pytest
from app.repositories.gestao.numero_modalidade_repository import NumeroModalidadeRepository
from app.schemas.gestao.numero_modalidade_schema import NumeroModalidadeRequest

@pytest.mark.asyncio
async def test_numero_modalidade_logic(db_session):
    repo = NumeroModalidadeRepository(db_session)
    id_modalidade = 1 # Mock
    
    # Valid Create
    res = await repo.get_or_create("10/2024", id_modalidade)
    assert res.id is not None
    assert res.numero == 10
    assert res.ano == 2024
    assert res.id_modalidade == id_modalidade
    
    # Existing
    res2 = await repo.get_or_create("10/2024", id_modalidade)
    assert res2.id == res.id
    
    # Invalid Format
    with pytest.raises(ValueError):
        await repo.get_or_create("INVALID", id_modalidade)
        
    with pytest.raises(ValueError):
        await repo.get_or_create("10-2024", id_modalidade)
