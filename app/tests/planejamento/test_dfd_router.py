import pytest
from httpx import AsyncClient
from datetime import date

# --- TESTES DE ROTEADOR (PLANEJAMENTO - DFD) ---

@pytest.mark.asyncio
async def test_criar_dfd_fluxo_completo(
    client: AsyncClient, 
    usuario_normal_token, 
    sample_unidade, 
    sample_user,
    sample_catalogo_item
):
    """
    Testa o fluxo completo de criação de um DFD via API.
    """
    # Payload alinhado com app/schemas/planejamento/dfd_schema.py (DFDCreate)
    payload = {
        "unidade_requisitante_id": sample_unidade.id, # Nome corrigido
        "responsavel_id": sample_user.id,             # Campo obrigatório adicionado
        "ano": 2024,                                  # Nome corrigido (era ano_pca)
        "data_req": str(date.today()),                # Campo obrigatório adicionado
        
        "objeto": "Contratação de Software de IA",    # Nome corrigido (era descricao_sucinta)
        "justificativa": "Automação de processos.",   # Nome corrigido (era justificativa_necessidade)
        
        # O Schema exige listas, mesmo que vazias, para equipe e dotações
        "equipe": [], 
        "dotacoes": [],
        
        # Itens do DFD
        "itens": [
            {
                "catalogo_item_id": sample_catalogo_item.id, # Nome corrigido (era id_catalogo_item)
                "quantidade": 10,
                "valor_unitario_estimado": 500.0
            }
        ]
    }

    # Enviando como usuário autenticado
    response = await client.post("/dfds/", json=payload, headers=usuario_normal_token)

    # Verificações
    if response.status_code != 201:
        # Debugging: imprime o erro real do Pydantic se falhar
        print(f"Erro ao criar DFD: {response.text}")

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["objeto"] == payload["objeto"]
    assert len(data.get("itens", [])) >= 1

@pytest.mark.asyncio
async def test_criar_dfd_erro_validacao(client: AsyncClient, usuario_normal_token):
    """
    Valida erro 422 ao tentar criar DFD com campos obrigatórios faltando.
    """
    payload_invalido = {
        "objeto": "DFD Incompleto"
        # Faltam muitos campos obrigatórios (ano, responsavel, etc)
    }

    response = await client.post("/dfds/", json=payload_invalido, headers=usuario_normal_token)
    
    # FastAPI retorna 422 para erros de validação Pydantic
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data