import pytest
from app.services.planejamento.dfd_service import DFDService
from app.schemas.planejamento.dfd_schema import DFDCreate

@pytest.mark.asyncio
async def test_dfd_service_crud(db_session, sample_unidade):
    service = DFDService()
    
    # Create
    dfd_in = DFDCreate(
        ano=2024, 
        id_unidade_requisitante=sample_unidade.id, 
        objeto="Service Test", 
        justificativa="J"
    )
    # Service methods seem to be synchronous wrappers calling Async Repos? 
    # Wait, the analyzed service code used `repo.create` which is async in previous repo view.
    # The Generic Repository is async.
    # `DFDService` defined methods without `async def`.
    # BUT `DFDRepository.create` is `async def`.
    # If the service methods are sync but call async methods without await, they return coroutines.
    # The service code I viewed:
    # def create_dfd(self, db, dfd_in): return repo.create(dfd_in)
    # This returns the coroutine object.
    # So in test we must await it.
    
    coro = service.create_dfd(db_session, dfd_in)
    new_dfd = await coro
    assert new_dfd.id is not None
    
    # Get
    coro = service.get_dfd(db_session, new_dfd.id)
    found = await coro
    assert found.id == new_dfd.id
