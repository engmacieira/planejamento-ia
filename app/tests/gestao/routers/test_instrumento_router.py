import pytest

@pytest.mark.asyncio
async def test_instrumento_router_ops(client, usuario_normal_token):
    pl = {"nome": "Inst Router Test", "ativo": True}
    r = await client.post("/instrumentos/", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    i_id = r.json()["id"]
    
    # Update
    r = await client.put(f"/instrumentos/{i_id}", json={"nome": "Inst Update"}, headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["nome"] == "Inst Update"
    
    # Delete
    r = await client.delete(f"/instrumentos/{i_id}", headers=usuario_normal_token)
    assert r.status_code == 204
