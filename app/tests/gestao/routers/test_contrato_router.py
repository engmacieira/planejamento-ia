import pytest
from datetime import date

@pytest.mark.asyncio
async def test_contrato_router_full_cycle(client, usuario_normal_token):
    # Create
    contrato_payload = {
        "numero_contrato": "999/2099",
        "ano": 2099,
        "objeto": "Router Integration Test",
        "fornecedor": "Fornecedor Router",
        "categoria_nome": "Cat Router",
        "instrumento_nome": "Inst Router",
        "modalidade_nome": "Mod Router",
        "numero_modalidade_str": "999/2099",
        "processo_licitatorio_numero": "999/2099",
        "valor_global": 10000.0,
        "ativo": True,
        "data_inicio": str(date.today()),
        "data_fim": str(date.today())
    }
    
    r = await client.post("/contratos/", json=contrato_payload, headers=usuario_normal_token)
    assert r.status_code == 201
    c_data = r.json()
    assert c_data["numero_contrato"] == "999/2099"
    c_id = c_data["id"]
    
    # Get by ID
    r = await client.get(f"/contratos/{c_id}", headers=usuario_normal_token)
    assert r.status_code == 200
    
    # Update
    update_data = {"objeto": "Updated Object", "numero_contrato": "999/2099"} # Fields required? Schema depends on PartialUpdate or Full? Schema shows ContratoUpdateRequest usually optional
    # Checking schema usage in router: ContratoUpdateRequest.
    # Assuming standard optional fields logic.
    r = await client.put(f"/contratos/{c_id}", json=update_data, headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["objeto"] == "Updated Object"
    
    # Activate/Deactivate
    r = await client.patch(f"/contratos/{c_id}/status?activate=false", headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["ativo"] is False
    
    # Delete
    r = await client.delete(f"/contratos/{c_id}", headers=usuario_normal_token)
    assert r.status_code == 204
