import pytest
from httpx import AsyncClient

# --- TESTES DE CORE (AUTH & USER) ---

@pytest.mark.asyncio
async def test_login_sucesso(client: AsyncClient, sample_user):
    """
    Testa o fluxo de login para obter access_token.
    """
    # Use as credenciais EXATAS definidas na fixture sample_user do conftest.py
    payload = {
        "username": sample_user.email, # <--- Usa o email real da fixture (teste@teste.com)
        "password": "123456"           # Senha padrão definida na fixture
    }

    response = await client.post("/token", data=payload)
    
    # Debug para ajudar caso falhe
    assert response.status_code == 200, f"Falha no login: {response.text}"
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_rota_protegida_sem_token(client: AsyncClient):
    """
    Tenta acessar rota protegida sem token e deve receber 401.
    """
    # Ajuste a rota se necessário. Se /users/me não existir, tente /users/
    response = await client.get("/users/me")
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

@pytest.mark.asyncio
async def test_rota_protegida_com_token(client: AsyncClient, usuario_normal_token, sample_user):
    """
    Acessa rota protegida com token válido.
    """
    response = await client.get("/users/me", headers=usuario_normal_token)
    
    assert response.status_code == 200, f"Erro na rota protegida: {response.text}"
    data = response.json()
    assert data["email"] == sample_user.email
    assert data["username"] == sample_user.username