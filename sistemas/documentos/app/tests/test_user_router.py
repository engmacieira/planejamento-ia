def test_create_user_route_success(client):
    """
    Testa se a rota POST /users/ cria o usuário e retorna 201.
    Isso cobre: user_router, deps, main (roteamento) e schemas (validação HTTP).
    """
    # Arrange
    payload = {
        "name": "Matheus API",
        "email": "api@teste.com",
        "password": "123"
    }

    # Act
    response = client.post("/users/", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "api@teste.com"
    assert "id" in data
    assert "password" not in data # Segurança: não pode voltar a senha

def test_create_user_route_duplicate_email(client):
    """
    Testa se a rota retorna 400 Bad Request quando email duplica.
    Isso cobre o bloco 'except' do router.
    """
    # 1. Cria o primeiro usuário
    payload = {"name": "User 1", "email": "duplo@api.com", "password": "123"}
    client.post("/users/", json=payload)

    # 2. Tenta criar o segundo igual
    response = client.post("/users/", json=payload)

    # 3. Verifica se tratou o erro
    assert response.status_code == 400
    assert response.json()["detail"] == "Erro ao criar usuário. Email já cadastrado?"