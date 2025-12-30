from app.models.planejamento.item_risco_model import ItemRisco

def test_item_risco_initialization():
    """
    Testa a inicialização de um Item de Risco.
    """
    desc = "Risco de atraso na entrega pelo fornecedor"
    prob = "Média"
    imp = "Alto"
    resp = "Fiscal do Contrato"
    matriz_id = 1
    
    risco = ItemRisco(
        matriz_id=matriz_id,
        descricao_risco=desc,
        probabilidade=prob,
        impacto=imp,
        responsavel=resp,
        # DefaultModel
        is_deleted=False
    )

    assert risco.descricao_risco == desc
    assert risco.probabilidade == prob
    assert risco.impacto == imp
    assert risco.matriz_id == matriz_id
    
    assert risco.is_deleted is False

def test_item_risco_nullable_fields():
    """
    Verifica se campos opcionais aceitam None.
    """
    risco = ItemRisco(
        matriz_id=1,
        descricao_risco="Risco Genérico",
        medida_preventiva=None
    )
    
    assert risco.medida_preventiva is None