from app.models.gestao.grupo_model import Grupo

def test_grupo_initialization():
    """
    Testa a inicialização de um Grupo de Material/Serviço.
    """
    cat_id = 1
    codigo = "05"
    nome = "Material de Limpeza"
    
    grupo = Grupo(
        categoria_id=cat_id,
        codigo=codigo,
        nome=nome,
        ativo=True,
        is_deleted=False
    )

    assert grupo.categoria_id == cat_id
    assert grupo.codigo == codigo
    assert grupo.nome == nome
    assert grupo.ativo is True
    
    assert grupo.is_deleted is False