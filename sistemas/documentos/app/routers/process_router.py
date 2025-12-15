from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
import os
import shutil
from datetime import datetime

from app.schemas.process_schema import ProcessoCreate, ProcessoResponse
from app.models.user_model import User
from app.repositories.process_repository import ProcessoRepository
from app.services.document_service import DocumentService
from app.services.zip_service import ZipService
from app.core.deps import get_current_user, get_db, get_document_service, get_zip_service

# Dependência manual para o Repo (se não tiver no deps.py ainda)
from sqlalchemy.orm import Session
def get_process_repo(db: Session = Depends(get_db)):
    return ProcessoRepository(db)

router = APIRouter(prefix="/processos", tags=["Processos"])

# --- ROTAS CRUD (Gerenciamento de Dados) ---

@router.post("/", status_code=201, response_model=ProcessoResponse)
def create_process(
    process_data: ProcessoCreate,
    current_user: User = Depends(get_current_user),
    repo: ProcessoRepository = Depends(get_process_repo)
):
    """Salva um novo processo no banco."""
    return repo.create(schema=process_data, owner_id=current_user.id)

@router.get("/", response_model=List[ProcessoResponse])
def list_processes(
    current_user: User = Depends(get_current_user),
    repo: ProcessoRepository = Depends(get_process_repo)
):
    """Lista todos os processos do usuário."""
    return repo.list_by_user(current_user.id)

# --- A ROTA MÁGICA (Geração em Lote) ---

@router.post("/{process_id}/gerar_zip")
def generate_process_documents(
    process_id: int,
    current_user: User = Depends(get_current_user),
    repo: ProcessoRepository = Depends(get_process_repo),
    doc_service: DocumentService = Depends(get_document_service),
    zip_service: ZipService = Depends(get_zip_service)
):
    """
    1. Busca o processo.
    2. Vai na pasta 'templates_padrao'.
    3. Preenche CADA arquivo com os dados do processo.
    4. Gera um ZIP e devolve para download.
    """
    # 1. Buscar Processo
    processo = repo.get_by_id(process_id)
    if not processo or processo.owner_id != current_user.id:
        raise HTTPException(404, "Processo não encontrado")

    # 2. Configurar Pastas
    BASE_TEMPLATES = "templates_padrao"
    OUTPUT_FOLDER = f"temp_output_{process_id}_{int(datetime.now().timestamp())}"
    
    if not os.path.exists(BASE_TEMPLATES):
        raise HTTPException(500, "Pasta de templates padrão não encontrada no servidor.")

    # Cria pasta temporária para salvar os arquivos gerados
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    try:
        # 3. Preparar o Dicionário de Dados
        # Transformamos o objeto do banco num dicionário simples para o replace
        # Ex: processo.numero_dfd -> "DFD": "038/2025"
        # Precisamos mapear os nomes das colunas para as Tags do Word
        data_map = {
            "numero_dfd": processo.numero_dfd,
            "secretaria": processo.secretaria,
            "objeto": processo.objeto,
            "valor_estimado": processo.valor_estimado,
            "valor_extenso": processo.valor_extenso,
            "dotacao": processo.dotacao,
            "artigo": processo.artigo,
            "data1": processo.data1,
            "data2": processo.data2,
            "data3": processo.data3,
            "data4": processo.data4,
            "data5": processo.data5,
            # ... adicione os outros campos se necessário
        }

        # 4. Loop de Geração
        files_generated = 0
        for filename in os.listdir(BASE_TEMPLATES):
            if filename.endswith(".docx") and not filename.startswith("~$"):
                input_path = os.path.join(BASE_TEMPLATES, filename)
                output_path = os.path.join(OUTPUT_FOLDER, filename)
                
                # CHAMA O MOTOR DE PREENCHIMENTO
                doc_service.fill_document(input_path, data_map, output_path)
                files_generated += 1

        if files_generated == 0:
            raise HTTPException(400, "Nenhum modelo .docx encontrado na pasta padrão.")

        # 5. Gerar ZIP
        zip_buffer = zip_service.create_zip_from_folder(OUTPUT_FOLDER)
        
        # Define o nome do arquivo baixado
        headers = {"Content-Disposition": f'attachment; filename="Processo_{processo.numero_dfd.replace("/", "-")}.zip"'}
        
        return StreamingResponse(zip_buffer, media_type="application/zip", headers=headers)

    finally:
        # 6. Limpeza (Housekeeping)
        # Apaga a pasta temporária de geração, independente de erro ou sucesso
        if os.path.exists(OUTPUT_FOLDER):
            shutil.rmtree(OUTPUT_FOLDER)