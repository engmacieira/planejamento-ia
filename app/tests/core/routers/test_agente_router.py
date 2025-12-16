import pytest

@pytest.mark.asyncio
async def test_core_agente_router(client, usuario_normal_token):
    # Create
    pl = {"nome": "Agente Core Test", "cargo": "Analista", "is_active": True, "email": "a@core.com"}
    r = await client.post("/agentes/", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    ag_id = r.json()["id"]
    
    # Get All
    r = await client.get("/agentes/", headers=usuario_normal_token)
    assert r.status_code == 200
    
    # Update
    r = await client.put(f"/agentes/{ag_id}", json={"cargo": "Gerente"}, headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["cargo"] == "Gerente"
    
    # Delete
    r = await client.delete(f"/agentes/{ag_id}", headers=usuario_normal_token)
    assert r.status_code == 204
