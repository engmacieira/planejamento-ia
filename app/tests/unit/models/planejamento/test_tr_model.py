from app.models.planejamento.tr_model import TR

def test_tr_initialization():
    """
    Testa a inicialização do Termo de Referência (TR).
    """
    matriz_id = 5
    txt_fundamentacao = "Baseado na Lei 14.133/2021, Art. 72..."
    
    tr = TR(
        matriz_id=matriz_id,
        fundamentacao=txt_fundamentacao,
        # DefaultModel
        is_deleted=False
    )

    assert tr.matriz_id == matriz_id
    assert tr.fundamentacao == txt_fundamentacao
    
    assert tr.is_deleted is False

def test_tr_nullable():
    """
    Verifica campos opcionais.
    """
    tr = TR(
        matriz_id=1,
        fundamentacao=None
    )
    
    assert tr.fundamentacao is None