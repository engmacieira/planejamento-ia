import pytest

@pytest.mark.asyncio
async def test_numero_modalidade_router(client, usuario_normal_token, sample_modalidade):
    # Create
    pl = {"numero_ano": "100/2024", "id_modalidade": sample_modalidade.id}
    r = await client.post("/numeros-modalidade/", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    nm_id = r.json()["id"]
    
    # Get All
    r = await client.get("/numeros-modalidade/", headers=usuario_normal_token)
    assert r.status_code == 200
    
    # Delete
    r = await client.delete(f"/numeros-modalidade/{nm_id}", headers=usuario_normal_token)
    assert r.status_code == 204
