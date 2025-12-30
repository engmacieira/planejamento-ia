from app.models.planejamento.etp_model import ETP

def test_etp_initialization():
    """
    Testa a inicialização do ETP.
    """
    nec = "Necessidade de renovação do parque tecnológico"
    tec = "Processadores i7, 16GB RAM"
    
    etp = ETP(
        descricao_necessidade=nec,
        requisitos_tecnicos=tec,
        viabilidade=True,
        is_deleted=False
    )

    assert etp.descricao_necessidade == nec
    assert etp.requisitos_tecnicos == tec
    assert etp.viabilidade is True
    
    assert etp.is_deleted is False

def test_etp_nullable_fields():
    """
    Verifica se campos opcionais aceitam None.
    """
    etp = ETP(
        descricao_necessidade="Teste",
        previsao_pca=None,
        impactos_ambientais=None
    )
    
    assert etp.previsao_pca is None
    assert etp.impactos_ambientais is None