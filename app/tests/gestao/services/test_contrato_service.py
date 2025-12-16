import pytest
from app.services.gestao.contrato_service import ContratoService
from app.schemas.gestao.contrato_schema import ContratoCreateRequest
from datetime import date, timedelta

@pytest.mark.asyncio
async def test_create_contrato_date_validation(db_session):
    service = ContratoService()
    
    # Needs valid data to pass Pydantic check before reaching service?
    # Service expects 'contrato_in'. Pydantic validation usually happens at Router.
    # Here we mock the object or use the schema.
    
    # Invalid dates
    c_in = ContratoCreateRequest(
        numero_contrato="1/2024",
        ano=2024,
        objeto="Objeto",
        fornecedor="F", category_nome="C", instrumento_nome="I", modalidade_nome="M", numero_modalidade_str="1/2024", processo_licitatorio_numero="1/24",
        data_inicio=date.today(),
        data_fim=date.today() - timedelta(days=1), # End before Start
        valor_global=100.0,
        ativo=True
    )
    
    # The service calls repo.create if valid.
    # But it should raise ValueError first.
    with pytest.raises(ValueError, match="data final"):
        service.create_contrato(db_session, c_in)

@pytest.mark.asyncio
async def test_get_contratos_vencendo_placeholder(db_session):
    service = ContratoService()
    res = service.get_contratos_vencendo(db_session)
    assert res == []

@pytest.mark.asyncio
async def test_calcular_saldo_placeholder(db_session):
    service = ContratoService()
    res = service.calcular_saldo(db_session, 1)
    assert res == 0.0
