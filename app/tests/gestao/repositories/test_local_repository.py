import pytest
from app.repositories.gestao.local_repository import LocalRepository
from app.schemas.gestao.local_schema import LocalRequest

@pytest.mark.asyncio
async def test_local_repository_flow(db_session):
    repo = LocalRepository(db_session)
    
    res = await repo.get_or_create("Almoxarifado Central")
    assert res.id is not None
    assert res.nome == "Almoxarifado Central"
    
    res2 = await repo.get_or_create("Almoxarifado Central")
    assert res2.id == res.id
    
    res3 = await repo.get_or_create("Novo Local")
    assert res3.id != res.id
