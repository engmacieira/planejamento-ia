import pytest

@pytest.mark.asyncio
async def test_core_auth_login(client, sample_user):
    # Login
    login_data = {"username": sample_user.email, "password": "password123"}
    r = await client.post("/token", data=login_data)
    assert r.status_code == 200
    token = r.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"
