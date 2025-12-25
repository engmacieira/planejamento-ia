import pytest

@pytest.mark.asyncio
async def test_item_router(client, usuario_normal_token):
    # Needs contract. Mock ID?
    # Router checks constraints? Likely yes if integrity error catch exists.
    # We can try to create if we have a valid contract from previous test fixture 'sample_contrato'.
    # In conftest 'sample_contrato' creates one but we need its ID.
    # Or create one here.
    
    # Let's create a minimal contract first via repository or assume fixure usage in params
    pass # Wait, how to access fixture in test body if not passed?
         # I need to add fixture to arg list.

@pytest.mark.asyncio
async def test_item_router_flow(client, usuario_normal_token, db_session, sample_instrumento, sample_categoria, sample_modalidade):
    # Need to setup a contract manually or via endpoint
    # Let's use endpoint to be integration-pure
    c_pl = {
        "numero_contrato": "ITEM-TEST/24",
        "ano": 2024,
        "objeto": "For Item Test",
        "fornecedor": "F", "categoria_nome": "C", "instrumento_nome": "I", "modalidade_nome": "M", "numero_modalidade_str": "1/24", "processo_licitatorio_numero": "1/24",
        "valor_global": 100.0,
        "ativo": True,
        "data_inicio": "2024-01-01", "data_fim": "2024-12-31"
    }
    r = await client.post("/contratos/", json=c_pl, headers=usuario_normal_token)
    c_id = r.json()["id"]
    
    # Create Item
    item_pl = {
        "id_contrato": c_id,
        "numero_item": 1,
        "descricao": "Item 1",
        "quantidade": 10,
        "valor_unitario": 5.0,
        "unidade_medida": "UN",
        "ativo": True
    }
    r = await client.post("/itens/", json=item_pl, headers=usuario_normal_token)
    assert r.status_code == 201
    i_id = r.json()["id"]
    
    # Get Itens by Contract
    r = await client.get(f"/itens/?contrato_id={c_id}", headers=usuario_normal_token)
    assert r.status_code == 200
    assert len(r.json()) == 1
    
    # Delete Item
    r = await client.delete(f"/itens/{i_id}", headers=usuario_normal_token)
    assert r.status_code == 204
