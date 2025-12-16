import pytest
from app.services.planejamento.processo_service import ProcessoService
from app.schemas.planejamento.processo_schema import ProcessoLicitatorioCreate
from app.models.planejamento.dfd_model import DFD

@pytest.mark.asyncio
async def test_processo_service_logic(db_session, sample_unidade):
    service = ProcessoService()
    
    # Setup DFD
    dfd = DFD(ano=2024, unidade_requisitante_id=sample_unidade.id, descricao_sucinta="For Proc", justificativa_necessidade="J", status="Aprovado")
    db_session.add(dfd)
    await db_session.commit()
    await db_session.refresh(dfd) # Get ID
    
    proc_in = ProcessoLicitatorioCreate(
        id_dfd=dfd.id,
        numero="PROC-SERVICE/2024",
        objeto="Objeto Service"
    )
    
    # Test Success
    # Note: Service methods are sync wrappers returning coroutines
    coro = service.create_processo(db_session, proc_in)
    proc = await coro
    assert proc.id is not None
    assert proc.id_dfd == dfd.id
    
    # Test Error: DFD Already Linked
    # Need to refresh DFD to see relationship?
    # Or creating a new process with same DFD id should fail
    # The logic checks 'if db_dfd.processo:'.
    # We need to ensure the relationship is loaded or updated.
    await db_session.refresh(dfd) 
    
    with pytest.raises(ValueError, match="already linked"):
        # Create another input with same DFD
        proc_in_2 = ProcessoLicitatorioCreate(id_dfd=dfd.id, numero="PROC-FAIL/2024", objeto="Fail")
        await service.create_processo(db_session, proc_in_2)

@pytest.mark.asyncio
async def test_processo_service_dfd_not_found(db_session):
    service = ProcessoService()
    proc_in = ProcessoLicitatorioCreate(id_dfd=99999, numero="PROC-404", objeto="404")
    
    with pytest.raises(ValueError, match="DFD not found"):
        await service.create_processo(db_session, proc_in)
