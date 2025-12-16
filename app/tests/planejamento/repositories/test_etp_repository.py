import pytest
from app.repositories.planejamento.etp_repository import ETPRepository
from app.repositories.planejamento.dfd_repository import DFDRepository
from app.schemas.planejamento.dfd_schema import DFDCreate, ItemDFDSchema

@pytest.mark.asyncio
async def test_consolidar_dfds(db_session, sample_unidade):
    dfd_repo = DFDRepository(db_session)
    etp_repo = ETPRepository(db_session)
    
    # Create 2 DFDs with same item to test summing
    item1 = ItemDFDSchema(catalogo_item_id=10, quantidade=5, valor_unitario_estimado=2.0)
    dfd1 = await dfd_repo.create(DFDCreate(ano=2024, id_unidade_requisitante=sample_unidade.id, objeto="D1", justificativa="J", itens=[item1]))
    
    item2 = ItemDFDSchema(catalogo_item_id=10, quantidade=3, valor_unitario_estimado=2.0)
    dfd2 = await dfd_repo.create(DFDCreate(ano=2024, id_unidade_requisitante=sample_unidade.id, objeto="D2", justificativa="J", itens=[item2]))
    
    # Consolidate
    etp = await etp_repo.consolidar_dfds([dfd1.id, dfd2.id])
    
    assert etp.id is not None
    # Check Items Sum: 5 + 3 = 8
    assert len(etp.itens) == 1
    assert etp.itens[0].quantidade_total == 8.0
    assert etp.itens[0].catalogo_item_id == 10
    
    # Check DFD status update
    await db_session.refresh(dfd1)
    await db_session.refresh(dfd2)
    assert dfd1.etp_id == etp.id
    assert dfd1.status == "Em ETP"

@pytest.mark.asyncio
async def test_unlink_dfd(db_session, sample_unidade):
    dfd_repo = DFDRepository(db_session)
    etp_repo = ETPRepository(db_session)
    
    dfd = await dfd_repo.create(DFDCreate(ano=2024, id_unidade_requisitante=sample_unidade.id, objeto="D", justificativa="J"))
    etp = await etp_repo.consolidar_dfds([dfd.id])
    
    # Unlink
    success = await etp_repo.unlink_dfd(etp.id, dfd.id)
    assert success is True
    
    await db_session.refresh(dfd)
    assert dfd.etp_id is None
    assert dfd.status == "Rascunho"
