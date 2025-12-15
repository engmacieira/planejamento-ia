from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List

from app.schemas.template_schema import TemplateResponse, TemplateCreate
from app.models.user_model import User
from app.repositories.template_repository import TemplateRepository
from app.services.file_service import FileService 
from app.core.deps import get_current_user, get_template_repo, get_file_service

router = APIRouter(prefix="/templates", tags=["Templates"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TemplateResponse)
def create_template(
    # Como é upload, não usamos Pydantic no corpo direto. Usamos Form e File.
    filename: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...), # <--- O Arquivo físico
    current_user: User = Depends(get_current_user),
    repo: TemplateRepository = Depends(get_template_repo),
    file_service: FileService = Depends(get_file_service) # <--- Injeção do Service
):
    # 1. Validar extensão
    if not file.filename.endswith(".docx"):
        raise HTTPException(400, "Apenas arquivos .docx são permitidos")

    # 2. Salvar arquivo físico (Service Layer)
    saved_path = file_service.save_upload(file)
    
    # 3. Preparar dados para o Repository
    # (Convertemos os dados do Form para o Schema que o repo espera)
    template_data = TemplateCreate(filename=filename, description=description)
    
    # 4. Salvar no Banco (Repository Layer)
    return repo.create(
        schema=template_data, 
        saved_path=saved_path, 
        owner_id=current_user.id
    )

@router.get("/", response_model=List[TemplateResponse])
def list_my_templates(
    current_user: User = Depends(get_current_user), # <--- Proteção
    repo: TemplateRepository = Depends(get_template_repo)
):
    """Lista apenas os templates do usuário logado."""
    return repo.list_by_user(current_user.id)

@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    repo: TemplateRepository = Depends(get_template_repo)
):
    """Soft delete de um template (apenas se for dono)."""
    # 1. Busca o template para ver se existe
    template = repo.get_by_id(template_id)
    
    # 2. Verifica se existe e se é DO USUÁRIO
    if not template or template.owner_id != current_user.id:
        # Segurança: Não dizemos se existe ou não, apenas damos 404
        raise HTTPException(status_code=404, detail="Template não encontrado")
        
    repo.delete(template_id)
    return None