import pytest
from app.repositories.gestao.user_repository import UserGestaoRepository
from app.models.core.user_model import User

@pytest.mark.asyncio
async def test_user_gestao_get_by_username(db_session, sample_user):
    repo = UserGestaoRepository(db_session)
    
    # Existing
    user = await repo.get_by_username("usuario_teste") 
    # Assumes sample_user fixture creates this user
    assert user is not None
    assert user.id == sample_user.id
    
    # Non-existent
    missing = await repo.get_by_username("ghost_user")
    assert missing is None
