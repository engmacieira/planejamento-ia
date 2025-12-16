import pytest

@pytest.mark.asyncio
async def test_modalidade_router_crud(client, usuario_normal_token):
    pl = {"nome": "Modalidade Router"}
    r = await client.post("/modalidades/", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    m_id = r.json()["id"]
    
    r = await client.get(f"/modalidades/{m_id}", headers=usuario_normal_token)
    assert r.status_code == 200
    
    r = await client.put(f"/modalidades/{m_id}", json={"nome": "Modalidade Update"}, headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["nome"] == "Modalidade Update"
    
    r = await client.delete(f"/modalidades/{m_id}", headers=usuario_normal_token)
    assert r.status_code == 204
