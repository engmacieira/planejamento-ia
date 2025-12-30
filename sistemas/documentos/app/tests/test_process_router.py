import pytest
from unittest.mock import patch, MagicMock
from app.models.user_model import User
from app.repositories.process_repository import ProcessoRepository
from app.schemas.process_schema import ProcessoCreate
from app.core.deps import get_current_user
from app.main import app

@pytest.fixture
def logged_user(db_session):
    user = User(name="Logged", email="logged@test.com", password_hash="123")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    app.dependency_overrides[get_current_user] = lambda: user
    yield user
    app.dependency_overrides.pop(get_current_user, None)

def test_create_process_endpoint(client, logged_user):
    """Testa o POST /processos/"""
    payload = {
        "numero_dfd": "500/2025",
        "secretaria": "Obras",
        "objeto": "Asfalto",
        "valor_estimado": "R$ 500k",
        "valor_extenso": "quinhentos mil"
    }
    
    response = client.post("/processos/", json=payload)
    
    assert response.status_code == 201
    assert response.json()["numero_dfd"] == "500/2025"

def test_generate_zip_endpoint_success(client, db_session, logged_user):
    """
    Testa o fluxo completo de geração de ZIP com Mocks.
    """
    repo = ProcessoRepository(db_session)
    processo = repo.create(ProcessoCreate(
        numero_dfd="ZIP_TEST", secretaria="S", objeto="O", 
        valor_estimado="V", valor_extenso="VE"
    ), logged_user.id)

    # Mocks para enganar o sistema de arquivos
    with patch("os.path.exists", return_value=True):
        with patch("os.makedirs"):
            with patch("os.listdir", return_value=["modelo.docx"]):
                with patch("app.services.document_service.DocumentService.fill_document") as mock_fill:
                    with patch("app.services.zip_service.ZipService.create_zip_from_folder", return_value=MagicMock()) as mock_zip:
                        # MOCK ESSENCIAL: Finge que deleta a pasta
                        with patch("shutil.rmtree"): 
                            
                            response = client.post(f"/processos/{processo.id}/gerar_zip")

                            assert response.status_code == 200
                            assert response.headers["content-type"] == "application/zip"
                            mock_fill.assert_called_once()

def test_generate_zip_process_not_found(client, logged_user):
    """Tenta gerar zip de um ID que não existe"""
    response = client.post("/processos/9999/gerar_zip")
    assert response.status_code == 404

def test_list_processes_endpoint(client, db_session, logged_user):
    """Testa a rota GET /processos/"""
    repo = ProcessoRepository(db_session)
    repo.create(ProcessoCreate(
        numero_dfd="001", secretaria="A", objeto="Obj A", valor_estimado="10", valor_extenso="dez"
    ), logged_user.id)
    repo.create(ProcessoCreate(
        numero_dfd="002", secretaria="B", objeto="Obj B", valor_estimado="20", valor_extenso="vinte"
    ), logged_user.id)

    response = client.get("/processos/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["numero_dfd"] == "001"

def test_generate_zip_template_folder_not_found(client, db_session, logged_user):
    """
    Simula que a pasta 'templates_padrao' não existe.
    """
    repo = ProcessoRepository(db_session)
    proc = repo.create(ProcessoCreate(
        numero_dfd="ERR", secretaria="S", objeto="O", valor_estimado="V", valor_extenso="VE"
    ), logged_user.id)

    # Mock condicional: Retorna False para templates_padrao, True para o resto (incluindo output folder)
    side_effect = lambda path: False if "templates_padrao" in str(path) else True

    with patch("os.path.exists", side_effect=side_effect):
        # Como o resto retorna True, ele vai tentar deletar o output folder no finally.
        # Precisamos mockar o rmtree para não explodir.
        with patch("shutil.rmtree"):
            response = client.post(f"/processos/{proc.id}/gerar_zip")
        
    assert response.status_code == 500
    assert response.json()["detail"] == "Pasta de templates padrão não encontrada no servidor."

def test_generate_zip_no_docx_files(client, db_session, logged_user):
    """
    Simula que a pasta existe, mas não tem arquivos .docx.
    """
    repo = ProcessoRepository(db_session)
    proc = repo.create(ProcessoCreate(
        numero_dfd="EMPTY", secretaria="S", objeto="O", valor_estimado="V", valor_extenso="VE"
    ), logged_user.id)

    with patch("os.path.exists", return_value=True):
        with patch("os.makedirs"):
            with patch("os.listdir", return_value=["~$temp.docx", "readme.txt"]):
                # MOCK NOVO AQUI TAMBÉM:
                with patch("shutil.rmtree"):
                    response = client.post(f"/processos/{proc.id}/gerar_zip")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Nenhum modelo .docx encontrado na pasta padrão."