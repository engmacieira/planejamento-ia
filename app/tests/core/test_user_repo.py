import pytest
from app.repositories.core.user_repository import UserRepository
from app.schemas.user_schema import UserCreate

@pytest.mark.asyncio
async def test_create_user(db_session):
    # db_session fixture should be async session from conftest if available, or we assume it is.
    # If not, we might need AsyncMock again if 'db' fixture is not fully async ready or if we prefer unit test.
    # Assuming integration test if 'db' fixture is used.
    
    repo = UserRepository(db_session)
    user_data = UserCreate(
        username="newuser_core", # Changing generic to be safe
        email="new_core@example.com",
        nome_completo="New User Core",
        password="securepassword"
    )
    
    user = await repo.create(user_data) # Renamed from create_user to create
    
    assert user.id is not None
    assert user.email == "new_core@example.com"
    assert user.username == "newuser_core"
    assert user.nome_completo == "New User Core"
    assert user.password_hash != "securepassword" # Should be hashed

@pytest.mark.asyncio
async def test_get_user_by_email(db_session, sample_user):
    # sample_user needs to be awaited if it relies on async creation, or if passed as scalar.
    # Usually fixtures run before test.
    
    repo = UserRepository(db_session)
    
    found_user = await repo.get_by_email(sample_user.email)
    assert found_user is not None
    assert found_user.id == sample_user.id
    
    not_found = await repo.get_by_email("doesnotexist@example.com")
    assert not_found is None
