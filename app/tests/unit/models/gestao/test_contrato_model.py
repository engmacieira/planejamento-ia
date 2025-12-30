from datetime import date, timedelta
from decimal import Decimal
from app.models.gestao.contrato_model import Contrato

def test_contrato_initialization():
    """
    Testa a inicialização de um Contrato com vigência e valores.
    """
    num_contrato = "100/2024"
    ano = 2024
    proc_id = 50
    forn_id = 10
    hoje = date.today()
    fim_ano = hoje + timedelta(days=365)
    valor = Decimal("500000.00")
    
    contrato = Contrato(
        numero_contrato=num_contrato,
        ano_contrato=ano,
        id_processo_licitatorio=proc_id,
        id_fornecedor=forn_id,
        data_assinatura=hoje,
        data_inicio_vigencia=hoje,
        data_fim_vigencia=fim_ano,
        valor_total=valor,
        ativo=True,
        is_deleted=False
    )

    assert contrato.numero_contrato == num_contrato
    assert contrato.valor_total == valor
    assert contrato.data_fim_vigencia > contrato.data_inicio_vigencia
    assert contrato.id_fornecedor == forn_id
    
    assert contrato.is_deleted is False

def test_contrato_nullable_relations():
    """
    Verifica se classificações opcionais (categoria, modalidade) aceitam None.
    """
    contrato = Contrato(
        numero_contrato="101/2024",
        ano_contrato=2024,
        id_processo_licitatorio=1,
        id_fornecedor=1,
        data_assinatura=date.today(),
        data_inicio_vigencia=date.today(),
        data_fim_vigencia=date.today(),
        id_categoria=None,
        id_modalidade=None
    )
    
    assert contrato.id_categoria is None
    assert contrato.id_modalidade is None