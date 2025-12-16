import shutil
import os
from fastapi import UploadFile
from uuid import uuid4

class FileService:
    def __init__(self, upload_dir: str = "uploads"):
        # Garante que a pasta de uploads existe
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_upload(self, file: UploadFile) -> str:
        """
        Salva o arquivo recebido no disco e retorna o caminho salvo.
        Gera um nome único para evitar conflitos (ex: dois arquivos 'contrato.docx').
        """
        # 1. Gera nome único (uuid) mantendo a extensão original
        extension = os.path.splitext(file.filename)[1]
        new_filename = f"{uuid4()}{extension}"
        file_path = os.path.join(self.upload_dir, new_filename)

        # 2. Salva o conteúdo físico
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return file_path
        
    def delete_file(self, path: str):
        """Remove o arquivo físico (usado quando deletamos o template)."""
        if os.path.exists(path):
            os.remove(path)
