import pytest

@pytest.mark.asyncio
async def test_core_user_router(client, usuario_normal_token):
    # Create
    pl = {
        "username": "core_user_test",
        "email": "coreuser@test.com",
        "password": "password123",
        "nome_completo": "Core User",
        "nivel_acesso": 1
    }
    r = await client.post("/users/", json=pl) # No auth needed usually, or admin?
    # Default core router usually public for registration or protected?
    # Checked code: create_user depends on get_async_user_repo, no auth dependency on route.
    assert r.status_code == 201
    
    # Me
    r = await client.get("/users/me", headers=usuario_normal_token)
    assert r.status_code == 200
    assert "email" in r.json()
