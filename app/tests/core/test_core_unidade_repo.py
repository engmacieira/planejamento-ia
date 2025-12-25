import pytest
from unittest.mock import MagicMock, AsyncMock
from app.repositories.core.unidade_repository import UnidadeRepository
from app.schemas.core.unidade_schema import UnidadeRequest
from app.models.core.unidade_model import Unidade

@pytest.mark.asyncio
async def test_create_unidade_mock():
    # Mock AsyncSession
    mock_session = AsyncMock()
    
    # Mock commit/refresh behaviors
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    mock_session.add = MagicMock() # Ensure add is synchronous
    
    # Since BaseRepository uses session.add(obj), we don't mock execute/scalars for create in the same way as get.
    # But we can verify session.add was called.
    
    repo = UnidadeRepository(mock_session)
    req = UnidadeRequest(nome="Secretaria Mock")
    
    # Call async method
    result = await repo.create(req)
    
    # Since we are mocking session, the ID won't be auto-generated unless we set it on the added object manually side_effect or check mock logic.
    # However, BaseRepository relies on DB to set ID. 
    # For unit test with mocks, we verify flow.
    
    assert isinstance(result, Unidade)
    assert result.nome == "Secretaria Mock"
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_unidade_by_id_mock():
    mock_session = AsyncMock()
    
    # Mock execution result
    mock_result = MagicMock()
    mock_obj = Unidade(id=99, nome="Unidade 99")
    mock_result.scalars.return_value.first.return_value = mock_obj
    mock_session.execute.return_value = mock_result
    
    repo = UnidadeRepository(mock_session)
    result = await repo.get_by_id(99)
    
    assert result.id == 99
    assert result.nome == "Unidade 99"
    mock_session.execute.assert_awaited_once()
