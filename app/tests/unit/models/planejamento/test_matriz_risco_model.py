from app.models.planejamento.matriz_risco_model import MatrizRisco

def test_matriz_risco_initialization():
    """
    Testa a inicialização da Matriz de Risco.
    """
    etp_id = 10
    
    matriz = MatrizRisco(
        etp_id=etp_id,
        is_deleted=False
    )

    assert matriz.etp_id == etp_id
    assert matriz.is_deleted is False