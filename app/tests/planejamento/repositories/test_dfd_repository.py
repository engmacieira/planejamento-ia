import pytest
from app.repositories.planejamento.dfd_repository import DFDRepository
from app.schemas.planejamento.dfd_schema import DFDCreate, ItemDFDSchema
from app.models.planejamento.dfd_model import DFD

@pytest.mark.asyncio
async def test_create_dfd_with_nested(db_session, sample_unidade):
    repo = DFDRepository(db_session)
    
    item_in = ItemDFDSchema(
        catalogo_item_id=1, # Mock ID
        quantidade=10,
        valor_unitario_estimado=5.0,
        complemento_descricao="Details"
    )
    
    dfd_in = DFDCreate(
        ano=2024,
        id_unidade_requisitante=sample_unidade.id,
        objeto="Test DFD",
        justificativa="Justify",
        itens=[item_in],
        equipe=[],
        dotacoes=[]
    )
    
    # Run Create
    new_dfd = await repo.create(dfd_in)
    
    assert new_dfd.id is not None
    assert new_dfd.descricao_sucinta == "Test DFD" # Mapped from 'objeto'
    assert new_dfd.unidade_requisitante_id == sample_unidade.id
    assert len(new_dfd.itens) == 1
    assert new_dfd.itens[0].quantidade == 10

@pytest.mark.asyncio
async def test_update_dfd(db_session, sample_unidade):
    repo = DFDRepository(db_session)
    dfd_in = DFDCreate(ano=2024, id_unidade_requisitante=sample_unidade.id, objeto="Original", justificativa="J")
    dfd = await repo.create(dfd_in)
    
    update_data = {"objeto": "Updated DFD"} # Schema fields might differ (objet -> descricao_sucinta internally handled by update?)
    # Validating repo.update logic: it sets attributes directly from dict.
    # So we should pass 'descricao_sucinta' if that's the model field, or rely on DFDCreate conversion if passed?
    # Repository update method takes a 'dfd_data: dict'.
    # It iterates key/value.
    # So we must pass model field names.
    
    update_dict = {"descricao_sucinta": "Updated DFD"}
    updated = await repo.update(dfd.id, update_dict)
    
    assert updated.descricao_sucinta == "Updated DFD"

@pytest.mark.asyncio
async def test_delete_dfd_soft(db_session, sample_unidade):
    repo = DFDRepository(db_session)
    dfd_in = DFDCreate(ano=2024, id_unidade_requisitante=sample_unidade.id, objeto="To Delete", justificativa="J")
    dfd = await repo.create(dfd_in)
    
    success = await repo.delete(dfd.id)
    assert success is True
    
    # Check it's gone from active
    found = await repo.get_by_id(dfd.id) # get_by_id filters is_active=True
    assert found is None
