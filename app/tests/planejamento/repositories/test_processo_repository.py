import pytest
from app.repositories.planejamento.processo_repository import ProcessoRepository
from app.schemas.planejamento.processo_schema import ProcessoCreate

@pytest.mark.asyncio
async def test_processo_flow(db_session, sample_user):
    repo = ProcessoRepository(db_session)
    
    p_in = ProcessoCreate(
        titulo="Processo Teste",
        descricao="Desc",
        tipo="Administrativo"
    )
    
    # Create
    proc = await repo.create_processo(p_in, owner_id=sample_user.id)
    assert proc.id is not None
    assert proc.owner_id == sample_user.id
    
    # List
    procs = await repo.list_by_user(sample_user.id)
    assert len(procs) >= 1
    assert procs[0].titulo == "Processo Teste"
