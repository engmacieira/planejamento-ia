from fastapi.testclient import TestClient
from app.main import app

# Criamos um "cliente fake" baseado no nosso app
client = TestClient(app)

def test_read_root():
    """
    Testa se a rota raiz (/) retorna 200 OK e a mensagem correta.
    """
    # Act: Fazemos uma requisição GET simulada
    response = client.get("/")

    # Assert: Verificamos o status HTTP e o conteúdo JSON
    assert response.status_code == 200
    assert response.json() == {"message": "API Online! Acesse /docs"}