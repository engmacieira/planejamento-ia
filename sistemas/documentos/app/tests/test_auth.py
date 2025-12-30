from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate

def test_login_success(client, db_session):
    """
    Cria usuário -> Faz Login -> Recebe Token
    """
    # 1. Cria usuário (Senha: 123)
    repo = UserRepository(db_session)
    repo.create_user(UserCreate(name="Login User", email="login@teste.com", password="123"))

    # 2. Tenta logar (POST /token usa Form-Data, não JSON!)
    # O TestClient aceita data=... para enviar form-data
    response = client.post(
        "/token", 
        data={"username": "login@teste.com", "password": "123"}
    )

    # 3. Valida
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_login_fail(client, db_session):
    """
    Tenta logar com senha errada
    """
    repo = UserRepository(db_session)
    repo.create_user(UserCreate(name="Login User", email="login@teste.com", password="123"))

    response = client.post(
        "/token", 
        data={"username": "login@teste.com", "password": "SENHA_ERRADA"}
    )

    assert response.status_code == 401