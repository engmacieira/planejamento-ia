import pytest
from app.repositories.gestao.ci_pagamento_repository import CiPagamentoRepository
from app.schemas.gestao.ci_pagamento_schema import CiPagamentoCreateRequest
from datetime import date

@pytest.mark.asyncio
async def test_ci_pagamento_create(db_session, sample_unidade):
    repo = CiPagamentoRepository(db_session)
    
    # Assuming basic creation implies we provide valid connected IDs or they are nullable/mocked.
    # In integration test with sqlite, FKs might be enforced.
    # Let's try to pass dummy IDs for simple fields if we don't have fixtures for everything yet.
    
    ci_in = CiPagamentoCreateRequest(
        numero_ci="CI/2024/001",
        ano=2024,
        id_unidade=sample_unidade.id,
        id_aocs=1, # Mock
        data_emissao=date.today(),
        assunto="Pagamento Teste",
        valor=1500.00,
        status="Emitida"
    )
    
    try:
        ci = await repo.create(ci_in)
        assert ci.id is not None
        assert ci.numero_ci == "CI/2024/001"
    except Exception as e:
        pytest.fail(f"Failed to create CI: {e}")
