import pytest

@pytest.mark.asyncio
async def test_auth_login_flow(client, sample_user):
    # Test Login
    login_data = {
        "username": "usuario_teste",
        "password": "123456" # Matches sample_user fixture
    }
    
    r = await client.post("/auth/login", data=login_data) # OAuth2 form data
    assert r.status_code == 200
    token = r.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"
    
    # Test Users Me
    headers = {"Authorization": f"Bearer {token['access_token']}"}
    r = await client.get("/auth/users/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["username"] == "usuario_teste"

@pytest.mark.asyncio
async def test_auth_login_failure(client):
    login_data = {
        "username": "usuario_teste",
        "password": "wrong_password"
    }
    r = await client.post("/auth/login", data=login_data)
    assert r.status_code == 401
