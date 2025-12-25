import pytest
from app.repositories.gestao.contrato_repository import ContratoRepository
from app.schemas.gestao.contrato_schema import ContratoCreateRequest
from datetime import date

@pytest.mark.asyncio
async def test_create_contrato_complex_dependencies(db_session):
    repo = ContratoRepository(db_session)
    
    # Provides strings for deps (Fornecedor, Categoria etc) to trigger get_or_create logic
    contrato_in = ContratoCreateRequest(
        numero_contrato="123/2024",
        ano=2024,
        objeto="Contrato de Teste Completo",
        
        # Dependencies by Name/String
        fornecedor="Fornecedor Auto Inc", 
        categoria_nome="Serviços TI",
        instrumento_nome="Termo de Contrato",
        modalidade_nome="Dispensa",
        numero_modalidade_str="001/2024",
        processo_licitatorio_numero="PROC-001/24",
        
        data_inicio=date.today(),
        data_fim=date.today(),
        valor_global=50000.00,
        ativo=True
    )
    
    # This should trigger full chain of creation
    contrato = await repo.create(contrato_in)
    
    assert contrato.id is not None
    assert contrato.numero_contrato == "123/2024"
    
    # Check if dependencies were created and linked
    assert contrato.id_fornecedor is not None
    assert contrato.id_categoria is not None
    assert contrato.id_instrumento_contratual is not None
    assert contrato.id_modalidade is not None
    
    # Verify eager loading or fetch to confirm names
    # (Checking if repo.create returns obj with relationship loaded - implementation did refresh, but relation access depends on lazy loading strategy in async)
    # Ideally we re-fetch with options, but let's check basic IDs first.

@pytest.mark.asyncio
async def test_get_all_contratos(db_session):
    repo = ContratoRepository(db_session)
    # Should be empty or have 1 if session persists (it converts to function scope, so empty)
    
    res = await repo.get_all(skip=0, limit=10)
    assert isinstance(res, list)
