import zipfile
import os
import io

class ZipService:
    def create_zip_from_folder(self, folder_path: str) -> io.BytesIO:
        """
        Lê todos os arquivos de uma pasta e cria um arquivo ZIP na memória RAM.
        Retorna o objeto de bytes pronto para download.
        """
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Adiciona o arquivo ao zip usando apenas o nome relativo (sem pastas do sistema)
                    zip_file.write(file_path, arcname=file)
                    
        zip_buffer.seek(0) # Volta o ponteiro para o início para leitura
        return zip_buffer