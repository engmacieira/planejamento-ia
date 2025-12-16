import pytest
from app.services.planejamento.modalidade_service import ModalidadeService
from app.schemas.gestao.modalidade_schema import ModalidadeBase # Verification needed on schema name

@pytest.mark.asyncio
async def test_modalidade_service(db_session):
    service = ModalidadeService()
    # Assuming ModalidadeBase has 'nome'
    # Check schema? Assuming based on router usage.
    # Router uses ModalidadeRequest. Service uses ModalidadeBase.
    # Let's mock the input object if it's Pydantic.
    
    class MockModalidadeIn:
        nome = "Mod Service Test"
        def model_dump(self): return {"nome": self.nome}

    # Or just use dict if the repo allows? Repo expects Pydantic typically or dict.
    # ModalidadeRepository calls .model_dump() usually if BaseRepository.
    # Let's try to import the correct schema or use a mock.
    from app.schemas.gestao.modalidade_schema import ModalidadeRequest
    
    mod_in = ModalidadeRequest(nome="Mod Service Test", sigla="MST")
    
    # Service returns coroutine
    coro = service.create_modalidade(db_session, mod_in)
    new_mod = await coro
    assert new_mod.id is not None
    
    coro = service.get_modalidades(db_session)
    lst = await coro
    assert len(lst) >= 1
