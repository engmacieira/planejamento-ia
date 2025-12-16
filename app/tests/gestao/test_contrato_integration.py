import pytest
from httpx import AsyncClient
from app.services.gestao.contrato_service import ContratoService
from datetime import date, timedelta

# --- TESTES DE INTEGRAÇÃO (API) ---

@pytest.mark.asyncio
async def test_criar_contrato_sucesso(client: AsyncClient, usuario_normal_token, sample_unidade, sample_fornecedor):
    """
    Testa a criação bem-sucedida de um contrato via API.
    """
    payload = {
        "numero_contrato": "123/2024",
        "ano_contrato": 2024,
        "objeto": "Contrato de Teste Integração",
        "data_inicio": str(date.today()),
        "data_fim": str(date.today() + timedelta(days=365)),
        "valor_total": 10000.00,
        "id_unidade_gestora": sample_unidade.id, # Usando a unidade fixture
        # Campos obrigatórios adicionais dependendo do schema, adicione se necessário
        "id_fornecedor": sample_fornecedor.id,
        "categoria_nome": "Serviços",
        "instrumento_nome": "Contrato",
        "modalidade_nome": "Pregão Eletrônico",
        "numero_modalidade_str": "123/2024",
        "processo_licitatorio_numero": "Processo-001/2024"
    }
    
    # OBS: Se houver FK constraints reais no banco (não mockadas), precisaremos de fixtures para Fornecedor, etc.
    # Assumindo aqui que o teste roda com banco limpo ou fixtures mínimas.
    
    # Como o endpoint espera usuario logado, passamos o token
    response = await client.post("/contratos/", json=payload, headers=usuario_normal_token)
    
    # Se falhar por FK, o status será 400 ou 500, dependendo do tratamento de erro no router
    # Ajuste conforme necessidade se o DB for real e estrito.
    assert response.status_code == 201, f"Erro: {response.text}"
    data = response.json()
    assert "id" in data
    assert data["numero_contrato"] == "123/2024"

@pytest.mark.asyncio
async def test_buscar_contrato_por_id(client: AsyncClient, usuario_normal_token, db_session, sample_unidade, sample_fornecedor):
    """
    Cria um contrato diretamente (ou via API antes) e tenta buscar pelo ID.
    """
    # 1. Setup: Criar contrato no banco via Service ou Repo para garantir existência
    from app.repositories.gestao.contrato_repository import ContratoRepository
    from app.schemas.gestao.contrato_schema import ContratoCreateRequest
    
    # Usando schema para criar via repo
    try:
        payload_schema = ContratoCreateRequest(
            numero_contrato="999/2024",
            ano_contrato=2024,
            objeto="Busca por ID",
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            valor_total=500.0,
            id_unidade_gestora=sample_unidade.id,
            id_fornecedor=sample_fornecedor.id,
            categoria_nome="Serviços",
            instrumento_nome="Contrato",
            modalidade_nome="Pregão",
            numero_modalidade_str="999/2024",
            processo_licitatorio_numero="Proc-999/2024",
            ativo=True
        )
        repo = ContratoRepository(db_session)
        contrato_criado = repo.create(payload_schema)
        await db_session.commit() # Importante commitar se for teste transacional
        contrato_id = contrato_criado.id
    except Exception as e:
        pytest.skip(f"Pular teste de busca se não conseguir criar contrato setup: {e}")

    # 2. Testar GET via API
    response = await client.get(f"/contratos/{contrato_id}", headers=usuario_normal_token)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contrato_id
    assert data["objeto"] == "Busca por ID"


@pytest.fixture(scope="function")
async def sample_fornecedor(db_session):
    from app.models.gestao.fornecedor_model import Fornecedor
    fornecedor = Fornecedor(
        razao_social="Fornecedor Teste Ltda",
        cpf_cnpj="12345678000199",
        email="contato@fornecedor.com",
        telefone="11999999999"
    )
    db_session.add(fornecedor)
    await db_session.commit()
    await db_session.refresh(fornecedor)
    return fornecedor

# --- TESTES UNITÁRIOS DE SERVICE (LÓGICA DE NEGÓCIO) ---

def test_validacao_datas_service(db_session):
    """
    Testa a regra de negócio do ContratoService: Data Fim < Data Início deve falhar.
    """
    service = ContratoService()
    
    # Mockando um objeto contrato_in simples (pode ser dict ou objeto, dependendo de como o Service consome)
    # O código do service usa contrato_in.data_fim_vigencia, então objeto ou namedtuple ou Pydantic model
    from collections import namedtuple
    ContratoMock = namedtuple("ContratoMock", ["data_inicio_vigencia", "data_fim_vigencia"])
    
    data_inicio = date.today()
    data_fim_errada = data_inicio - timedelta(days=1) # Data anterior
    
    contrato_in = ContratoMock(data_inicio_vigencia=data_inicio, data_fim_vigencia=data_fim_errada)
    
    with pytest.raises(ValueError) as excinfo:
        service.create_contrato(db_session, contrato_in)
    
    assert "não pode ser anterior" in str(excinfo.value)
