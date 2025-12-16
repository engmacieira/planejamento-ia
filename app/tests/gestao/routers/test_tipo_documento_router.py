import pytest

@pytest.mark.asyncio
async def test_tipo_documento_router(client, usuario_normal_token):
    pl = {"nome": "Tipo Doc Router", "descricao": "Desc"}
    r = await client.post("/tipos-documento/", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    tid = r.json()["id"]
    
    r = await client.get(f"/tipos-documento/{tid}", headers=usuario_normal_token)
    assert r.status_code == 200
    
    r = await client.delete(f"/tipos-documento/{tid}", headers=usuario_normal_token)
    assert r.status_code == 204
