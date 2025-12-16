import pytest

@pytest.mark.asyncio
async def test_core_unidade_router(client, usuario_normal_token):
    # Create
    pl = {"nome": "Unidade Core Test", "sigla": "UCT", "codigo": "999"}
    r = await client.post("/unidades/", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    u_id = r.json()["id"]
    
    # Get All
    r = await client.get("/unidades/", headers=usuario_normal_token)
    assert r.status_code == 200
    
    # Update
    r = await client.put(f"/unidades/{u_id}", json={"sigla": "UPD"}, headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["sigla"] == "UPD"
    
    # Delete
    r = await client.delete(f"/unidades/{u_id}", headers=usuario_normal_token)
    assert r.status_code == 204
