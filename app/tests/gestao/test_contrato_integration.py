import pytest
from httpx import AsyncClient
from datetime import date, timedelta
from app.repositories.gestao.contrato_repository import ContratoRepository
from app.schemas.gestao.contrato_schema import ContratoCreateRequest

# --- TESTES DE INTEGRAÇÃO (API) ---

@pytest.mark.asyncio
async def test_criar_contrato_sucesso(
    client: AsyncClient, 
    usuario_normal_token, 
    sample_unidade, 
    sample_fornecedor,
    sample_categoria,     # Garante categoria válida
    sample_instrumento,   # Garante instrumento válido
    sample_modalidade,    # Garante modalidade válida
    sample_processo       # Garante Processo (e DFD) válidos
):
    """
    Testa a criação bem-sucedida de um contrato via API.
    A API espera receber Strings para Categoria, Instrumento, etc., 
    e o Repo faz o 'get_or_create'. Como as fixtures já criaram,
    o Repo vai apenas fazer o 'get' e tudo funcionará.
    """
    
    # Formata numero do processo conforme esperado pelo parser do repo (ex: "1/2024")
    processo_str = f"{sample_processo.numero_processo}/{sample_processo.ano_processo}"

    payload = {
        "numero_contrato": "123/2024",
        "ano_contrato": 2024,
        "data_assinatura": str(date.today()),
        "objeto": "Contrato de Teste Integração",
        "data_inicio": str(date.today()),
        "data_fim": str(date.today() + timedelta(days=365)),
        "valor_total": 10000.00,
        "id_unidade_gestora": sample_unidade.id,
        "id_fornecedor": sample_fornecedor.id,
        
        # Usamos os nomes exatos criados nas fixtures para garantir o match
        "categoria_nome": sample_categoria.nome,
        "instrumento_nome": sample_instrumento.nome,
        "modalidade_nome": sample_modalidade.nome,
        "numero_modalidade_str": "999/2024", # Esse o sistema pode criar novo sem problemas (geralmente não tem FK complexa)
        
        # Aqui passamos a string que referencia o Processo+DFD já existentes
        "processo_licitatorio_numero": processo_str
    }
    
    response = await client.post("/contratos/", json=payload, headers=usuario_normal_token)
    
    # Debug: Se falhar, mostra o erro retornado pela API
    assert response.status_code == 201, f"Erro API: {response.text}"
    
    data = response.json()
    assert "id" in data
    assert data["numero_contrato"] == "123/2024"
    # Verifica se ele vinculou corretamente ao processo existente
    assert data["id_processo_licitatorio"] == sample_processo.id

@pytest.mark.asyncio
async def test_buscar_contrato_por_id(
    client: AsyncClient, 
    usuario_normal_token, 
    db_session, 
    sample_unidade, 
    sample_fornecedor,
    sample_categoria,
    sample_instrumento,
    sample_modalidade,
    sample_processo
):
    """
    Cria um contrato diretamente via Repository e tenta buscar pelo ID na API.
    """
    repo = ContratoRepository(db_session)
    
    processo_str = f"{sample_processo.numero_processo}/{sample_processo.ano_processo}"

    # Setup: Criar contrato no banco
    # Note que usamos await repo.create, pois é async
    try:
        payload_schema = ContratoCreateRequest(
            numero_contrato="999/2024",
            ano_contrato=2024,
            data_assinatura=date.today(),
            objeto="Busca por ID",
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=30),
            valor_total=500.0,
            id_unidade_gestora=sample_unidade.id,
            id_fornecedor=sample_fornecedor.id,
            categoria_nome=sample_categoria.nome,
            instrumento_nome=sample_instrumento.nome,
            modalidade_nome=sample_modalidade.nome,
            numero_modalidade_str="888/2024",
            processo_licitatorio_numero=processo_str,
            ativo=True
        )
        
        # AQUI estava o erro de "coroutine never awaited" anteriormente
        contrato_criado = await repo.create(payload_schema) 
        await db_session.commit()
        
        contrato_id = contrato_criado.id
    except Exception as e:
        pytest.fail(f"Erro no setup do teste (criação direta): {e}")

    # Testar GET via API
    response = await client.get(f"/contratos/{contrato_id}", headers=usuario_normal_token)
    
    assert response.status_code == 200, f"Erro API GET: {response.text}"
    data = response.json()
    assert data["id"] == contrato_id
    assert data["objeto"] == "Busca por ID"

# --- TESTES UNITÁRIOS DE SERVICE ---

def test_validacao_datas_service():
    """
    Testa apenas a lógica pura, sem banco de dados.
    """
    from app.services.gestao.contrato_service import ContratoService
    
    # Mock simples
    class MockContrato:
        def __init__(self, inicio, fim):
            self.data_inicio_vigencia = inicio
            self.data_fim_vigencia = fim

    service = ContratoService()
    
    data_inicio = date.today()
    data_fim_errada = data_inicio - timedelta(days=1)
    
    # Como o service espera session, passamos None pois a validação de data ocorre antes do flush no DB
    # Nota: Se o seu service tentar usar db_session antes da validação, esse teste unitário precisará de ajuste.
    # Mas para lógica pura de data, isso costuma bastar.
    contrato_in = MockContrato(data_inicio, data_fim_errada)
    
    with pytest.raises(ValueError) as excinfo:
        # Assumindo que o método é create_contrato(db, obj_in)
        service.create_contrato(None, contrato_in)
    
    assert "não pode ser anterior" in str(excinfo.value)