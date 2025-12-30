from app.models.planejamento.dfd_equipe_model import DFDEquipe

def test_dfd_equipe_initialization():
    """
    Testa a inicialização da Equipe de Planejamento do DFD.
    """
    dfd_id = 1
    agente_id = 10
    papel = "Integrante Técnico"
    
    membro = DFDEquipe(
        dfd_id=dfd_id,
        agente_id=agente_id,
        papel=papel,
        # DefaultModel
        is_deleted=False
    )

    assert membro.dfd_id == dfd_id
    assert membro.agente_id == agente_id
    assert membro.papel == papel
    
    assert membro.is_deleted is False