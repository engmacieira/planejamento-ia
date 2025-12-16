import pytest
from app.repositories.gestao.modalidade_repository import ModalidadeRepository
from app.schemas.gestao.modalidade_schema import ModalidadeRequest

@pytest.mark.asyncio
async def test_modalidade_crud(db_session):
    repo = ModalidadeRepository(db_session)
    
    # Create
    m_in = ModalidadeRequest(nome="Pregão Presencial")
    mod = await repo.create(m_in)
    assert mod.id is not None
    assert mod.nome == "Pregão Presencial"
    
    # Get by Nome
    fetched = await repo.get_by_nome("Pregão Presencial")
    assert fetched.id == mod.id
    
    # Get or Create
    goc = await repo.get_or_create("Pregão Presencial")
    assert goc.id == mod.id
    
    goc_new = await repo.get_or_create("Concorrência")
    assert goc_new.id != mod.id
    assert goc_new.nome == "Concorrência"
