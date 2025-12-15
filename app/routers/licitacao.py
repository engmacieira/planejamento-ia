from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas import licitacao as schemas
from app.services.licitacao.dfd_service import DFDService
from app.services.licitacao.processo_service import ProcessoService
from app.services.licitacao.modalidade_service import ModalidadeService

router = APIRouter(prefix="/licitacao", tags=["licitacao"])

dfd_service = DFDService()
processo_service = ProcessoService()
modalidade_service = ModalidadeService()

# --- DFDs ---
@router.post("/dfds/", response_model=schemas.DFD)
def create_dfd(dfd: schemas.DFDCreate, db: Session = Depends(get_db)):
    return dfd_service.create_dfd(db, dfd)

@router.get("/dfds/", response_model=List[schemas.DFD])
def read_dfds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return dfd_service.get_dfds(db, skip, limit)

@router.get("/dfds/{dfd_id}", response_model=schemas.DFD)
def read_dfd(dfd_id: int, db: Session = Depends(get_db)):
    dfd = dfd_service.get_dfd(db, dfd_id)
    if dfd is None:
        raise HTTPException(status_code=404, detail="DFD not found")
    return dfd

@router.put("/dfds/{dfd_id}", response_model=schemas.DFD)
def update_dfd_status(dfd_id: int, status_update: schemas.AFDUpdate, db: Session = Depends(get_db)):
    updated_dfd = dfd_service.update_status(db, dfd_id, status_update)
    if not updated_dfd:
        raise HTTPException(status_code=404, detail="DFD not found")
    return updated_dfd

@router.post("/dfds/{dfd_id}/itens/", response_model=schemas.ItemDFD)
def create_item_dfd(dfd_id: int, item: schemas.ItemDFDCreate, db: Session = Depends(get_db)):
    new_item = dfd_service.add_item(db, dfd_id, item)
    if not new_item:
        raise HTTPException(status_code=404, detail="DFD not found")
    return new_item

# --- Modalidades ---
@router.post("/modalidades/", response_model=schemas.Modalidade)
def create_modalidade(modalidade: schemas.ModalidadeBase, db: Session = Depends(get_db)):
    return modalidade_service.create_modalidade(db, modalidade)

@router.get("/modalidades/", response_model=List[schemas.Modalidade])
def read_modalidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return modalidade_service.get_modalidades(db, skip, limit)

# --- Processos ---
@router.post("/processos/", response_model=schemas.ProcessoLicitatorio)
def create_processo(processo: schemas.ProcessoLicitatorioCreate, db: Session = Depends(get_db)):
    try:
        return processo_service.create_processo(db, processo)
    except ValueError as e:
         raise HTTPException(status_code=400, detail=str(e))

@router.get("/processos/", response_model=List[schemas.ProcessoLicitatorio])
def read_processos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return processo_service.get_processos(db, skip, limit)

@router.get("/processos/{processo_id}", response_model=schemas.ProcessoLicitatorio)
def read_processo(processo_id: int, db: Session = Depends(get_db)):
    processo = processo_service.get_processo(db, processo_id)
    if processo is None:
        raise HTTPException(status_code=404, detail="Processo not found")
    return processo
