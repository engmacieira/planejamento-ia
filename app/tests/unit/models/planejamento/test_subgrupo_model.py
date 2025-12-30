from app.models.planejamento.subgrupo_model import Subgrupo

def test_subgrupo_initialization():
    """
    Testa a inicialização de um Subgrupo de Material/Serviço.
    """
    grupo_id = 5
    codigo = "12"
    nome = "Papelaria"
    
    sub = Subgrupo(
        grupo_id=grupo_id,
        codigo=codigo,
        nome=nome,
        # DefaultModel
        ativo=True,
        is_deleted=False
    )

    assert sub.grupo_id == grupo_id
    assert sub.codigo == codigo
    assert sub.nome == nome
    assert sub.ativo is True
    
    assert sub.is_deleted is False