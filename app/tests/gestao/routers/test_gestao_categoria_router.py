import pytest

@pytest.mark.asyncio
async def test_categoria_router_crud(client, usuario_normal_token):
    # Create
    data = {"nome": "Cat Router", "codigo_taxonomia": "R"}
    r = await client.post("/categorias/", json=data, headers=usuario_normal_token)
    assert r.status_code == 201
    cat_id = r.json()["id"]
    
    # Toggle Status
    r = await client.patch(f"/categorias/{cat_id}/status?activate=false", headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["ativo"] is False
    
    # Delete
    r = await client.delete(f"/categorias/{cat_id}", headers=usuario_normal_token)
    assert r.status_code == 204
