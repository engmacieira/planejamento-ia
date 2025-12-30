import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from fastapi import UploadFile
from io import BytesIO
from app.services.file_service import FileService

# Mockamos o os.makedirs para ele não criar a pasta 'uploads' de verdade no seu projeto durante o teste
@pytest.fixture
def mock_makedirs():
    with patch("os.makedirs") as mock:
        yield mock

def test_file_service_init(mock_makedirs):
    """Testa se ao iniciar, ele tenta criar a pasta de uploads."""
    service = FileService(upload_dir="pasta_teste")
    mock_makedirs.assert_called_with("pasta_teste", exist_ok=True)

def test_save_upload_logic(mock_makedirs):
    """
    Testa as linhas 18-26: Gerar nome e salvar bytes.
    """
    service = FileService()
    
    # 1. Cria um arquivo fake na memória
    conteudo = b"dados binarios"
    arquivo_upload = UploadFile(filename="relatorio.docx", file=BytesIO(conteudo))

    # 2. A Mágica: Mockamos o 'open' do sistema e o 'shutil'
    # mock_open: finge que abriu um arquivo
    # patch(shutil): finge que copiou os dados
    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("shutil.copyfileobj") as mocked_shutil:
            
            # Act
            caminho_salvo = service.save_upload(arquivo_upload)
            
            # Assert
            # Verifica se o caminho retornado contém a pasta e a extensão certa
            assert "uploads" in caminho_salvo
            assert caminho_salvo.endswith(".docx")
            
            # Verifica se o Python tentou abrir o arquivo em modo escrita binária ('wb')
            mocked_file.assert_called_once()
            args, _ = mocked_file.call_args
            assert args[1] == "wb"
            
            # Verifica se ele tentou copiar os dados
            mocked_shutil.assert_called_once()

def test_delete_file_exists(mock_makedirs):
    """
    Testa linhas 30-31 (Caminho True): Arquivo existe e deve ser deletado.
    """
    service = FileService()
    caminho = "uploads/teste.docx"

    # Mockamos path.exists para retornar True
    with patch("os.path.exists", return_value=True):
        with patch("os.remove") as mocked_remove:
            
            service.delete_file(caminho)
            
            # Deve ter chamado o remove
            mocked_remove.assert_called_once_with(caminho)

def test_delete_file_not_exists(mock_makedirs):
    """
    Testa linhas 30-31 (Caminho False): Arquivo não existe, não faz nada.
    """
    service = FileService()
    caminho = "uploads/fantasma.docx"

    # Mockamos path.exists para retornar False
    with patch("os.path.exists", return_value=False):
        with patch("os.remove") as mocked_remove:
            
            service.delete_file(caminho)
            
            # NÃO deve ter chamado o remove
            mocked_remove.assert_not_called()