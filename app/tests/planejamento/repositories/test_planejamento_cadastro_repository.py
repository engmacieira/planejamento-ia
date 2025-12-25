import pytest
from app.repositories.planejamento.cadastro_repository import CadastroRepository
from app.models.core.unidade_model import Unidade

@pytest.mark.asyncio
async def test_get_all_unidades(db_session):
    # Setup - assuming some seed data or create if empty
    # For integration tests, we can just call it. If it returns list, good.
    repo = CadastroRepository(db_session)
    res = await repo.get_all_unidades()
    # It might be empty if DB is fresh, but should run without error
    assert isinstance(res, list)

@pytest.mark.asyncio
async def test_get_all_itens(db_session):
    repo = CadastroRepository(db_session)
    res = await repo.get_all_itens()
    assert isinstance(res, list)
    if res:
        assert "nome" in res[0]
