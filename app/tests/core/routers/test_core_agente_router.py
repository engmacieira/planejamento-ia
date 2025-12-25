import pytest
from fastapi import status

# NÃO importe TestClient aqui. Vamos usar a fixture 'client' do conftest.
# NÃO faça overrides manuais aqui. O conftest já cuida disso.

@pytest.mark.asyncio
async def test_core_agente_router(client, db_session):
    """
    Testa a criação de um agente.
    Argumentos:
        client: Fixture injetada pelo conftest (já autenticada como Admin).
        db_session: Fixture de banco de dados limpo.
    """
    # 1. Setup - Dados para enviar
    payload = {
        "nome": "Agente 007",
        "cargo": "Espião",
        "email": "bond@mi6.uk",
        # Adicione outros campos obrigatórios do seu AgenteSchema aqui
    }

    # 2. Execução
    # O client já tem o UserMock injetado no header/dependência
    response = await client.post("/agentes/", json=payload) 
    # Obs: Verifique se a rota é "/agentes/" ou "/api/v1/agentes/" no seu main.py

    # 3. Verificação (Asserts)
    if response.status_code != status.HTTP_201_CREATED:
        # Dica de Debug: Se falhar, printa o erro para vermos no log
        print(f"Erro na API: {response.json()}")

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == "Agente 007"
    assert "id" in data