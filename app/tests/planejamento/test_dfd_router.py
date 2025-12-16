import pytest
from httpx import AsyncClient

# --- TESTES DE ROTEADOR (PLANEJAMENTO - DFD) ---

@pytest.mark.asyncio
async def test_criar_dfd_fluxo_completo(client: AsyncClient, usuario_normal_token, sample_unidade):
    """
    Testa o fluxo completo de criação de um DFD via API.
    """
    payload = {
        "id_unidade_requisitante": sample_unidade.id, 
        "descricao_sucinta": "Contratação de Software de IA",
        "justificativa_necessidade": "Necessário para automação de processos.",
        "alinhamento_estrategico": "Melhoria da eficiência operacional.",
        "resultados_esperados": "Redução de 50% no tempo de planejamento.",
        "data_previsão_conclusão": "2024-12-31",
        "ano_pca": 2024,
        # Itens do DFD
        "itens": [
            {
                "id_catalogo_item": 1, # Mock
                "descricao_complementar": "Licença enterprise",
                "quantidade": 10,
                "valor_unitario_estimado": 500.0,
                "codigo_item_catalogo": "12345"
            }
        ]
    }

    # Enviando como usuário autenticado
    response = await client.post("/dfds/", json=payload, headers=usuario_normal_token)

    # Verificações
    if response.status_code != 201:
        # Debugging: print error if fails
        print(f"Erro ao criar DFD: {response.text}")

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["descricao_sucinta"] == payload["descricao_sucinta"]
    assert len(data.get("itens", [])) >= 1

@pytest.mark.asyncio
async def test_criar_dfd_erro_validacao(client: AsyncClient, usuario_normal_token):
    """
    Valida erro 422 ao tentar criar DFD com campos obrigatórios faltando.
    """
    payload_invalido = {
        "descricao_sucinta": "DFD Incompleto"
        # Faltam muitos campos obrigatórios
    }

    response = await client.post("/dfds/", json=payload_invalido, headers=usuario_normal_token)
    
    # FastAPI retorna 422 para erros de validação Pydantic
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # FastAPI validation error structure
