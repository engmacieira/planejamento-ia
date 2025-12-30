from app.models.planejamento.etp_equipe_model import ETPEquipe

def test_etp_equipe_initialization():
    """
    Testa a inicialização da Equipe de Planejamento do ETP.
    """
    etp_id = 10
    agente_id = 5
    papel = "Relator Técnico"
    
    membro = ETPEquipe(
        etp_id=etp_id,
        agente_id=agente_id,
        papel=papel,
        is_deleted=False
    )

    assert membro.etp_id == etp_id
    assert membro.agente_id == agente_id
    assert membro.papel == papel
    
    assert membro.is_deleted is False