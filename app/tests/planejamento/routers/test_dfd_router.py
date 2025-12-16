import pytest

@pytest.mark.asyncio
async def test_dfd_router_crud(client, usuario_normal_token, sample_unidade):
    # Create
    pl = {
        "ano": 2024,
        "id_unidade_requisitante": sample_unidade.id,
        "objeto": "DFD Router Test",
        "justificativa": "J",
        "itens": [],
        "equipe": [],
        "dotacoes": []
    }
    r = await client.post("/dfds/", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    dfd_id = r.json()["id"]
    
    # Get All
    r = await client.get("/dfds/", headers=usuario_normal_token)
    assert r.status_code == 200
    
    # Get One
    r = await client.get(f"/dfds/{dfd_id}", headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["descricao_sucinta"] == "DFD Router Test"
    
    # Update
    update_pl = {"objeto": "Updated DFD Router", "status": "Em ETP"}
    r = await client.put(f"/dfds/{dfd_id}", json=update_pl, headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["descricao_sucinta"] == "Updated DFD Router"
    
    # Delete
    r = await client.delete(f"/dfds/{dfd_id}", headers=usuario_normal_token)
    assert r.status_code == 200 # Router sends 200 with message
    
    # Verify Deletion (Get One -> 404 or filter check)
    r = await client.get(f"/dfds/{dfd_id}", headers=usuario_normal_token)
    assert r.status_code == 404
