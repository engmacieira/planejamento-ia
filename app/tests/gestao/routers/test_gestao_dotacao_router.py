import pytest

@pytest.mark.asyncio
async def test_dotacao_router_crud(client, usuario_normal_token):
    # Create
    pl = {"info_orcamentaria": "Detalhe da Dotação", "descricao": "Desc"}
    r = await client.post("/dotacoes/", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    d_id = r.json()["id"]
    
    # Get All
    r = await client.get("/dotacoes/", headers=usuario_normal_token)
    assert r.status_code == 200
    assert len(r.json()) > 0
    
    # Delete
    r = await client.delete(f"/dotacoes/{d_id}", headers=usuario_normal_token)
    assert r.status_code == 204
