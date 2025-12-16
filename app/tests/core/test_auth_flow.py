import pytest
from httpx import AsyncClient

# --- TESTES DE CORE (AUTH & USER) ---

@pytest.mark.asyncio
async def test_login_sucesso(client: AsyncClient, sample_user):
    """
    Testa o fluxo de login para obter access_token.
    """
    # Credenciais padrão do sample_user (conftest via get_password_hash("123456"))
    payload = {
        "username": "test@example.com", # Auth route usa email como username
        "password": "123456"
    }

    # Endpoint OAuth2 form-urlencoded padrão
    response = await client.post("/token", data=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_rota_protegida_sem_token(client: AsyncClient):
    """
    Tenta acessar rota protegida sem token e deve receber 401.
    """
    # Tentando acessar /users/me do UserRouter (assumindo prefixo, ou rota raiz se dependente de include)
    # IMPORTANTE: Verifique o prefixo exato em main.py ou user_router.py. 
    # Em main.py: app.include_router(user_router.router)
    # Em user_router.py: geralmente user_router não tem prefixo ou é /users
    # Vamos tentar /users/me, se falhar 404 a gente ajusta, mas a regra é 401 pra falta de credencial.
    
    response = await client.get("/users/me")
    
    # Se a rota não existir seria 404, mas se existir e proteger, deve ser 401.
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_rota_protegida_com_token(client: AsyncClient, usuario_normal_token, sample_user):
    """
    Acessa rota protegida com token válido e verifica sucesso.
    """
    response = await client.get("/users/me", headers=usuario_normal_token)
    
    # Se obtiver 200, validamos que o usuário retornado é o correto
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user.email
    assert data["username"] == sample_user.username
