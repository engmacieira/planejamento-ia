from app.models.planejamento.dfd_dotacao_model import DFDDotacao

def test_dfd_dotacao_initialization():
    """
    Testa a inicialização da ligação DFD <-> Dotação.
    """
    dfd_id = 1
    dotacao_id = 99
    
    dfd_dotacao = DFDDotacao(
        dfd_id=dfd_id,
        dotacao_id=dotacao_id,
        is_deleted=False
    )

    assert dfd_dotacao.dfd_id == dfd_id
    assert dfd_dotacao.dotacao_id == dotacao_id
    
    assert dfd_dotacao.is_deleted is False