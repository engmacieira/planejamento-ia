from decimal import Decimal
from app.models.gestao.dotacao_model import Dotacao

def test_dotacao_initialization():
    """
    Testa a inicialização de uma Dotação Orçamentária.
    """
    exercicio = 2024
    codigo = "10.302.0001.2005"
    saldo = Decimal("50000.00")
    ficha = 1234
    
    dotacao = Dotacao(
        exercicio=exercicio,
        codigo_dotacao=codigo,
        numero_ficha=ficha,
        saldo_inicial=saldo,
        # Defaults explícitos para memória
        ativo=True,
        is_deleted=False
    )

    assert dotacao.exercicio == exercicio
    assert dotacao.codigo_dotacao == codigo
    assert dotacao.saldo_inicial == saldo
    assert dotacao.numero_ficha == ficha
    
    assert dotacao.ativo is True
    assert dotacao.is_deleted is False

def test_dotacao_nullable_fields():
    """
    Verifica se campos opcionais aceitam None.
    """
    dotacao = Dotacao(
        exercicio=2024,
        codigo_dotacao="COD-TEST",
        numero_ficha=None,
        descricao=None
    )
    
    assert dotacao.numero_ficha is None
    assert dotacao.descricao is None