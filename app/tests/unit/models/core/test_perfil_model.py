from app.models.core.perfil_model import Perfil

def test_perfil_model_initialization():
    """
    Testa a inicialização do Perfil e a herança do DefaultModel.
    """
    nome_perfil = "Administrador"
    desc = "Acesso total ao sistema"
    
    perfil = Perfil(
        nome=nome_perfil,
        descricao=desc,
        ativo=True,
        is_deleted=False
    )

    assert perfil.nome == nome_perfil
    assert perfil.descricao == desc
    assert perfil.ativo is True
    
    assert perfil.is_deleted is False

def test_perfil_nullable_fields():
    """
    Verifica se campos opcionais (descricao) aceitam None.
    """
    perfil = Perfil(
        nome="Visitante",
        descricao=None
    )
    
    assert perfil.descricao is None