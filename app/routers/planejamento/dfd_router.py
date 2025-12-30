from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.deps import get_db 
from app.repositories.planejamento.dfd_repository import DFDRepository
from app.schemas.planejamento.dfd_schema import DFDCreate, DFDResponse, DFDUpdate, DFDItemUpdatePrice

router = APIRouter(
    prefix="/dfds",
    tags=["Planejamento - DFD"]
)

@router.post("/", response_model=DFDResponse, status_code=status.HTTP_201_CREATED)
async def create_dfd(dfd: DFDCreate, db: AsyncSession = Depends(get_db)):
    """
    Cria um novo DFD com seus itens, equipe e dotação.
    """
    repo = DFDRepository(db) # <--- Instanciando corretamente
    return await repo.create(dfd)

@router.get("/", response_model=List[DFDResponse])
async def read_dfds(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Lista todos os DFDs ativos.
    """
    repo = DFDRepository(db) # <--- Instanciando corretamente
    return await repo.get_all(skip=skip, limit=limit)

@router.get("/{dfd_id}", response_model=DFDResponse)
async def read_dfd(dfd_id: int, db: AsyncSession = Depends(get_db)):
    """
    Busca um DFD específico pelo ID.
    """
    repo = DFDRepository(db) # <--- Instanciando corretamente
    db_dfd = await repo.get_by_id(dfd_id)
    
    if db_dfd is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="DFD não encontrado"
        )
    return db_dfd

@router.put("/{dfd_id}", response_model=DFDResponse)
async def update_dfd(dfd_id: int, dfd_update: DFDUpdate, db: AsyncSession = Depends(get_db)):
    """
    Atualiza um DFD existente.
    """
    repo = DFDRepository(db) # <--- Instanciando corretamente
    
    # O Repositório espera um dict para atualização customizada
    update_data = dfd_update.model_dump(exclude_unset=True)
    
    updated_dfd = await repo.update(dfd_id, update_data)
    
    if not updated_dfd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="DFD não encontrado para atualização"
        )
        
    return updated_dfd

@router.put("/itens/precos", status_code=status.HTTP_200_OK)
async def update_dfd_item_prices(itens: List[DFDItemUpdatePrice], db: AsyncSession = Depends(get_db)):
    """Recebe uma lista de {id, valor} e atualiza no banco."""
    repo = DFDRepository(db) # <--- Instanciando corretamente
    await repo.update_item_prices(itens)
    return {"message": "Preços atualizados com sucesso"}

@router.delete("/{dfd_id}")
async def deletar_dfd(dfd_id: int, db: AsyncSession = Depends(get_db)):
    repo = DFDRepository(db) # <--- Instanciando corretamente
    try:
        success = await repo.delete(dfd_id)
        if not success:
             raise HTTPException(status_code=404, detail="DFD não encontrado")
        return {"message": "DFD enviado para lixeira."}
    except Exception as e:
        # Pega mensagens de erro do repositório (ex: DFD vinculado a ETP)
        raise HTTPException(status_code=400, detail=str(e))