import pytest
from app.repositories.gestao.instrumento_repository import InstrumentoRepository
from app.schemas.gestao.instrumento_schema import InstrumentoRequest

@pytest.mark.asyncio
async def test_instrumento_logic(db_session):
    repo = InstrumentoRepository(db_session)
    
    input_data = InstrumentoRequest(nome="Aditivo", ativo=True)
    inst = await repo.create(input_data)
    assert inst.id is not None
    
    # Get by Nome
    found = await repo.get_by_nome("Aditivo")
    assert found.id == inst.id
    
    # Get Or Create
    goc = await repo.get_or_create("Aditivo")
    assert goc.id == inst.id
    
    new_goc = await repo.get_or_create("Apostilamento")
    assert new_goc.id != inst.id
    assert new_goc.nome == "Apostilamento"
