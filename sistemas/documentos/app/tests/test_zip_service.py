import pytest
import os
import zipfile
import io
from app.services.zip_service import ZipService

def test_create_zip_from_folder(tmp_path):
    """
    Testa se o serviço compacta arquivos corretamente.
    Usamos a fixture 'tmp_path' do pytest que cria uma pasta temporária real
    que se autodestrói após o teste.
    """
    # 1. Setup: Criar uma pasta com arquivos fake
    folder = tmp_path / "arquivos_para_zipar"
    folder.mkdir()
    
    # Cria arquivo 1
    file1 = folder / "contrato.txt"
    file1.write_text("conteudo do contrato")
    
    # Cria arquivo 2
    file2 = folder / "anexo.txt"
    file2.write_text("conteudo do anexo")

    # 2. Act: Chamar o serviço
    service = ZipService()
    zip_bytes = service.create_zip_from_folder(str(folder))

    # 3. Assert: Verificar se o binário é um ZIP válido
    assert isinstance(zip_bytes, io.BytesIO)
    
    # Abre o zip na memória para conferir o conteúdo
    with zipfile.ZipFile(zip_bytes, "r") as zf:
        lista_arquivos = zf.namelist()
        
        # Tem que ter os dois arquivos lá dentro
        assert "contrato.txt" in lista_arquivos
        assert "anexo.txt" in lista_arquivos
        
        # O conteúdo deve estar preservado
        assert zf.read("contrato.txt") == b"conteudo do contrato"