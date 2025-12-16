import pytest

@pytest.mark.asyncio
async def test_cadastro_routes(client, usuario_normal_token):
    # Secretarias
    r = await client.get("/cadastros/secretarias/", headers=usuario_normal_token)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    
    # Agentes
    r = await client.get("/cadastros/agentes/", headers=usuario_normal_token)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    
    # Itens
    r = await client.get("/cadastros/itens/", headers=usuario_normal_token)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    
    # Dotacoes
    r = await client.get("/cadastros/dotacoes/", headers=usuario_normal_token)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
