from app.models.planejamento.etp_dotacao_model import ETPDotacao

def test_etp_dotacao_initialization():
    """
    Testa a inicialização da ligação ETP <-> Dotação.
    """
    etp_id = 10
    dotacao_id = 55
    
    etp_dotacao = ETPDotacao(
        etp_id=etp_id,
        dotacao_id=dotacao_id,
        is_deleted=False
    )

    assert etp_dotacao.etp_id == etp_id
    assert etp_dotacao.dotacao_id == dotacao_id
    
    assert etp_dotacao.is_deleted is False