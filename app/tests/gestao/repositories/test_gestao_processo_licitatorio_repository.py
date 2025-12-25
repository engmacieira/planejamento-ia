import pytest
from app.repositories.gestao.processo_licitatorio_repository import ProcessoLicitatorioRepository

@pytest.mark.asyncio
async def test_processo_licitatorio_get_or_create(db_session):
    repo = ProcessoLicitatorioRepository(db_session)
    
    # Valid
    proc = await repo.get_or_create("123/2024")
    assert proc.id is not None
    assert proc.numero_processo == 123
    assert proc.ano_processo == 2024
    assert "Processo criado" in proc.objeto
    
    # Fetch Existing
    proc2 = await repo.get_or_create("123/2024")
    assert proc2.id == proc.id
    
    # Invalid
    res = await repo.get_or_create("INVALID")
    assert res is None
