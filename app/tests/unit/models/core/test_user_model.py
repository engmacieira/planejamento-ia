from datetime import datetime
from werkzeug.security import generate_password_hash
from app.models.core.user_model import User

def test_user_model_initialization():
    """
    Testa se o modelo User pode ser instanciado corretamente.
    """
    username = "testuser"
    email = "test@example.com"
    password_hash = "hashed_secret"
    nome_completo = "Test User"
    
    user = User(
        username=username, 
        email=email, 
        password_hash=password_hash,
        nome_completo=nome_completo,
        is_deleted=False 
    )

    assert user.username == username
    assert user.email == email
    assert user.nome_completo == nome_completo
    
    assert user.is_deleted is False

def test_user_password_verification():
    """
    Testa o método verificar_senha do modelo User.
    """
    senha_plana = "minha_senha_forte"
    senha_errada = "senha_errada"
    user = User(
        password_hash=generate_password_hash(senha_plana),
        username="auth_test",
        email="auth@test.com",
        nome_completo="Auth Test"
    )

    assert user.verificar_senha(senha_plana) is True
    assert user.verificar_senha(senha_errada) is False

def test_user_is_active_property():
    """
    Testa a property is_active.
    """
    user_ativo = User(ativo=True)
    user_inativo = User(ativo=False)

    assert user_ativo.is_active is True
    assert user_inativo.is_active is False