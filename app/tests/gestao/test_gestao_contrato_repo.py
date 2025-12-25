import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import date
from app.repositories.gestao.contrato_repository import ContratoRepository
from app.schemas.gestao.contrato_schema import ContratoCreateRequest
from app.models.gestao.contrato_model import Contrato

@pytest.mark.asyncio
async def test_create_contrato_mock():
    # Mock Async Session
    mock_session = AsyncMock()
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    mock_session.add = MagicMock() # Ensure add is synchronous
    
    repo = ContratoRepository(mock_session)
    
    # Mocking internal sub-repositories properly
    repo.fornecedor_repo = MagicMock()
    repo.fornecedor_repo.get_or_create = AsyncMock(return_value=MagicMock(id=5))
    
    repo.categoria_repo = MagicMock()
    repo.categoria_repo.get_or_create = AsyncMock(return_value=MagicMock(id=1))
    
    repo.instrumento_repo = MagicMock()
    repo.instrumento_repo.get_or_create = AsyncMock(return_value=MagicMock(id=1))
    
    repo.modalidade_repo = MagicMock()
    repo.modalidade_repo.get_or_create = AsyncMock(return_value=MagicMock(id=1))
    
    repo.numero_modalidade_repo = MagicMock()
    repo.numero_modalidade_repo.get_or_create = AsyncMock(return_value=MagicMock(id=1))
    
    repo.processo_licitatorio_repo = MagicMock()
    repo.processo_licitatorio_repo.get_or_create = AsyncMock(return_value=MagicMock(id=1))
    
    req = ContratoCreateRequest(
        numero_contrato="12345", 
        ano_contrato=2024,             
        data_assinatura=date.today(),
        data_inicio="2024-01-01",
        data_fim="2024-12-31",
        categoria_nome="Serviços",
        instrumento_nome="Contrato",
        modalidade_nome="Pregão",
        numero_modalidade_str="01/2024",
        processo_licitatorio_numero="PROC-001/2024",
        fornecedor={'nome': 'Fornecedor Mock Generic', 'cpf_cnpj': '00000000000000', 'nome_fantasia': 'Fornecedor Mock', 'razao_social': 'Mock SA', 'email': 'teste@teste.com', 'telefone': '1111'}, 
        id_fornecedor=5,
        objeto="Objeto Contrato"
    )
    
    result = await repo.create(req)
    
    # Check simple assignment
    assert isinstance(result, Contrato)
    assert result.numero_contrato == "12345"
    assert result.id_fornecedor == 5
    
    mock_session.add.assert_called()
    mock_session.commit.assert_awaited()
