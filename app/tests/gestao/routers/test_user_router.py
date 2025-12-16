import pytest

@pytest.mark.asyncio
async def test_user_router_admin_flow(client, admin_token):
    # Create User
    new_user = {
        "username": "router_test_user",
        "email": "router@test.com",
        "password": "password123",
        "nome_completo": "Router Test User",
        "nivel_acesso": 2
    }
    
    r = await client.post("/users/", json=new_user, headers=admin_token)
    assert r.status_code == 201
    uid = r.json()["id"]
    
    # Get User
    r = await client.get(f"/users/{uid}", headers=admin_token)
    assert r.status_code == 200
    assert r.json()["username"] == "router_test_user"
    
    # Update User
    update_pl = {"nome_completo": "Updated Name"}
    r = await client.put(f"/users/{uid}", json=update_pl, headers=admin_token)
    assert r.status_code == 200
    assert r.json()["nome_completo"] == "Updated Name"
    
    # Reset Password
    r = await client.post(f"/users/{uid}/reset-password", headers=admin_token)
    assert r.status_code == 200
    assert "new_password" in r.json()
    
    # Delete (Deactivate)
    r = await client.delete(f"/users/{uid}", headers=admin_token)
    assert r.status_code == 204

@pytest.mark.asyncio
async def test_user_router_no_admin(client, usuario_normal_token):
    r = await client.get("/users/", headers=usuario_normal_token)
    assert r.status_code == 403
