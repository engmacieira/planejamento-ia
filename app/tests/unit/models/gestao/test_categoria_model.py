from app.models.gestao.categoria_model import Categoria

def test_categoria_initialization():
    """
    Testa a inicialização da Categoria (Planejamento).
    """
    nome = "Material de Consumo"
    taxonomia = "01"
    
    categoria = Categoria(
        nome=nome,
        codigo_taxonomia=taxonomia,
        # DefaultModel
        ativo=True,
        is_deleted=False
    )

    assert categoria.nome == nome
    assert categoria.codigo_taxonomia == taxonomia
    assert categoria.ativo is True
    
    assert categoria.is_deleted is False