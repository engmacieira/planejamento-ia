from app.models.planejamento.numero_modalidade_model import NumeroModalidade

def test_numero_modalidade_initialization():
    """
    Testa a inicialização do sequencial de numeração da modalidade.
    """
    id_mod = 1
    numero = 15
    ano = 2024
    
    seq = NumeroModalidade(
        id_modalidade=id_mod,
        numero=numero,
        ano=ano,
        is_deleted=False
    )

    assert seq.id_modalidade == id_mod
    assert seq.numero == numero
    assert seq.ano == ano
    
    assert seq.is_deleted is False