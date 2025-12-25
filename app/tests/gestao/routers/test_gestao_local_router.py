import pytest

@pytest.mark.asyncio
async def test_local_router_crud(client, usuario_normal_token):
    pl = {"descricao": "Local Router"}
    r = await client.post("/locais/", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    l_id = r.json()["id"]
    
    r = await client.put(f"/locais/{l_id}", json={"descricao": "Local Update"}, headers=usuario_normal_token)
    assert r.status_code == 200
    
    r = await client.delete(f"/locais/{l_id}", headers=usuario_normal_token)
    assert r.status_code == 204
