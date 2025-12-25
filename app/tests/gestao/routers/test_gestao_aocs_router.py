import pytest

@pytest.mark.asyncio
async def test_aocs_crud_router(client, usuario_normal_token, db_session):
    # Create
    aocs_data = {
        "numero_aocs": "AOCS-ROUTER-01",
        "ano": 2024,
        "id_dfd": 1,
        "objeto": "Router Test",
        "justificativa": "J",
        "valor_estimado": 100.0,
        "unidade_requisitante": "Unit Router",
        "local_entrega": "Local Router",
        "agente_responsavel": "Agente Router",
        "dotacao_orcamentaria": "Dot Router"
    }
    
    r = await client.post("/aocs/", json=aocs_data, headers=usuario_normal_token)
    assert r.status_code == 201
    created = r.json()
    assert created["numero_aocs"] == "AOCS-ROUTER-01"
    id_aocs = created["id"]
    
    # Get All
    r = await client.get("/aocs/", headers=usuario_normal_token)
    assert r.status_code == 200
    assert len(r.json()) >= 1
    
    # Get By ID
    r = await client.get(f"/aocs/{id_aocs}", headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["id"] == id_aocs
    
    # Update not implemented in router? Checked code: yes it has PUT /{id}
    update_data = {"objeto": "Updated Router"}
    r = await client.put(f"/aocs/{id_aocs}", json=update_data, headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["objeto"] == "Updated Router"
    
    # Delete
    r = await client.delete(f"/aocs/{id_aocs}", headers=usuario_normal_token)
    assert r.status_code == 204
    
    # Verify Delete
    r = await client.get(f"/aocs/{id_aocs}", headers=usuario_normal_token)
    assert r.status_code == 404
