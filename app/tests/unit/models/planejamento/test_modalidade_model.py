from app.models.planejamento.modalidade_model import Modalidade

def test_modalidade_initialization():
    """
    Testa a inicialização de uma Modalidade de Licitação.
    """
    nome = "Pregão Eletrônico"
    sigla = "PE"
    lei = "Lei 14.133/2021"
    
    modalidade = Modalidade(
        nome=nome,
        sigla=sigla,
        fundamentacao_legal=lei,
        ativo=True,
        is_deleted=False
    )

    assert modalidade.nome == nome
    assert modalidade.sigla == sigla
    assert modalidade.fundamentacao_legal == lei
    assert modalidade.ativo is True
    
    assert modalidade.is_deleted is False