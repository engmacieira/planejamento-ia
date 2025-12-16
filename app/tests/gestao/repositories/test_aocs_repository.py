import pytest
from app.repositories.gestao.aocs_repository import AocsRepository
from app.schemas.gestao.aocs_schema import AocsCreateRequest
from datetime import date

@pytest.mark.asyncio
async def test_create_aocs_full(db_session, sample_unidade, sample_user): # Assuming user can act as Agente? Or need sample_agente
    repo = AocsRepository(db_session)
    
    # We strictly need Agente, Local, Dotacao to be resolved.
    # The repo creates them if they act as "get_or_create" strings?
    # Looking at code: yes, if string, repo.unidade_repo.get_or_create(...)
    
    # Creating with strings to test auto-resolution
    aocs_in = AocsCreateRequest(
        numero_aocs="AOCS-2024/001",
        ano=2024,
        id_dfd=1, # Mock ID
        objeto="Objeto Teste",
        justificativa="Justificativa Teste",
        valor_estimado=1000.00,
        unidade_requisitante="Unidade Nova Auto", # Should create
        local_entrega="Almoxarifado Central", # Should create
        agente_responsavel="Agente 007", # Should create
        dotacao_orcamentaria="Dotacao 2024" # Should create
    )
    
    # Note: Linked Repos (UnidadeRepo etc) must support get_or_create(str).
    # Assuming they do based on AocsRepository logic reading.
    
    try:
        aocs = await repo.create(aocs_in)
        assert aocs.id is not None
        assert aocs.numero_aocs == "AOCS-2024/001"
        assert aocs.id_unidade_requisitante is not None
        assert aocs.id_local_entrega is not None
    except Exception as e:
        pytest.fail(f"Could not create AOCS: {e}")

@pytest.mark.asyncio
async def test_create_aocs_existing_ids(db_session, sample_unidade):
    repo = AocsRepository(db_session)
    
    # Create with existing ID for unit
    # Others as strings
    aocs_in = AocsCreateRequest(
        numero_aocs="AOCS-2024/002",
        ano=2024,
        id_dfd=2,
        objeto="Objeto 2",
        justificativa="J2",
        valor_estimado=500.0,
        unidade_requisitante=sample_unidade.id, # Passing int ID
        local_entrega="Local 2",
        agente_responsavel="Agente 2",
        dotacao_orcamentaria="Dot 2"
    )
    
    aocs = await repo.create(aocs_in)
    assert aocs.id is not None
    assert aocs.id_unidade_requisitante == sample_unidade.id
