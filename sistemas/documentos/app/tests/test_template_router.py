import pytest
from io import BytesIO
from unittest.mock import patch
from app.models.user_model import User
from app.repositories.template_repository import TemplateRepository
from app.schemas.template_schema import TemplateCreate
from app.core.deps import get_current_user
from app.main import app

# --- FIXTURES ---
@pytest.fixture
def logged_user(db_session):
    """Cria um usuário e força o login dele no sistema."""
    user = User(name="Logged", email="logged@test.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Override global para os testes que usarem essa fixture
    app.dependency_overrides[get_current_user] = lambda: user
    yield user
    # Limpa depois
    app.dependency_overrides.pop(get_current_user, None)

# --- TESTES ---

def test_create_template_endpoint_with_upload(client, db_session, logged_user):
    """
    Testa o upload de arquivo via API.
    Agora enviamos Multipart/Form-Data em vez de JSON.
    """
    # 1. Preparar o Arquivo Fake
    file_content = b"conteudo binario do docx fake"
    filename = "contrato_v1.docx"
    
    # Formato do files: {'nome_campo': ('nome_arquivo', conteudo, 'tipo_mime')}
    files = {
        "file": (filename, BytesIO(file_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    }
    
    # Campos de texto vão no 'data' (Form Data)
    data = {
        "filename": filename,
        "description": "Upload via Teste"
    }

    # 2. Mock do FileService (Para não salvar no disco de verdade)
    # Dizemos: "Quando o save_upload for chamado, retorne essa string e não faça mais nada"
    with patch("app.services.file_service.FileService.save_upload", return_value="/tmp/fake_uuid.docx"):
        response = client.post("/templates/", data=data, files=files)

    # 3. Validações
    assert response.status_code == 201
    resp_json = response.json()
    assert resp_json["filename"] == filename
    assert resp_json["path"] == "/tmp/fake_uuid.docx" # Verifica se usou o retorno do Mock

def test_create_template_invalid_extension(client, logged_user):
    """Testa se a API bloqueia arquivos que não são .docx"""
    files = {
        "file": ("virus.exe", BytesIO(b"lixo"), "application/octet-stream")
    }
    data = {"filename": "virus.exe"}

    # Não precisamos mockar o save_upload porque a validação deve falhar ANTES de tentar salvar
    response = client.post("/templates/", data=data, files=files)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Apenas arquivos .docx são permitidos"

def test_list_templates_endpoint(client, db_session, logged_user):
    """Testa a listagem."""
    # Setup: Criar dados direto no banco (mais rápido e seguro que via API)
    repo = TemplateRepository(db_session)
    repo.create(TemplateCreate(filename="t1.docx"), "/path1", logged_user.id)
    repo.create(TemplateCreate(filename="t2.docx"), "/path2", logged_user.id)

    response = client.get("/templates/")
    
    assert response.status_code == 200
    assert len(response.json()) == 2

# --- Testes de Delete (Mantidos iguais, pois usam repo direto) ---
def test_delete_template_success(client, db_session, logged_user):
    repo = TemplateRepository(db_session)
    template = repo.create(TemplateCreate(filename="del.docx"), "/path", logged_user.id)

    response = client.delete(f"/templates/{template.id}")
    assert response.status_code == 204
    
    check = repo.get_by_id(template.id)
    assert check.is_deleted is True

def test_delete_template_not_found(client, logged_user):
    response = client.delete("/templates/9999")
    assert response.status_code == 404