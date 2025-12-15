from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.database import get_db
from app import models
from app.schemas import gestao as schemas

router = APIRouter(prefix="/gestao", tags=["gestao"])

# --- Fornecedores ---
@router.post("/fornecedores/", response_model=schemas.Fornecedor)
def create_fornecedor(fornecedor: schemas.FornecedorCreate, db: Session = Depends(get_db)):
    db_fornecedor = models.Fornecedor(**fornecedor.model_dump())
    db.add(db_fornecedor)
    db.commit()
    db.refresh(db_fornecedor)
    return db_fornecedor

@router.get("/fornecedores/", response_model=List[schemas.Fornecedor])
def read_fornecedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Fornecedor).offset(skip).limit(limit).all()

# --- Instrumentos Contratuais ---
@router.post("/instrumentos/", response_model=schemas.InstrumentoContratual)
def create_instrumento(instrumento: schemas.InstrumentoContratualCreate, db: Session = Depends(get_db)):
    db_instrumento = models.InstrumentoContratual(**instrumento.model_dump())
    db.add(db_instrumento)
    db.commit()
    db.refresh(db_instrumento)
    return db_instrumento

@router.get("/instrumentos/", response_model=List[schemas.InstrumentoContratual])
def read_instrumentos(db: Session = Depends(get_db)):
    return db.query(models.InstrumentoContratual).all()

# --- Contratos ---
@router.post("/contratos/", response_model=schemas.Contrato)
def create_contrato(contrato: schemas.ContratoCreate, db: Session = Depends(get_db)):
    # 1. Validate Process exists
    db_processo = db.query(models.ProcessoLicitatorio).filter(models.ProcessoLicitatorio.id == contrato.id_processo_licitatorio).first()
    if not db_processo:
        raise HTTPException(status_code=404, detail="Processo Licitatório not found")

    # 2. Operations (Transaction)
    # Extract itens
    itens_data = contrato.itens
    contrato_data = contrato.model_dump()
    contrato_data.pop('itens')
    
    db_contrato = models.Contrato(**contrato_data)
    db.add(db_contrato)
    db.commit() # Commit to get ID
    db.refresh(db_contrato)
    
    # 3. Add Itens
    try:
        total_contrato = 0
        for item in itens_data:
            # TODO: Validate if item belongs to the DFD linked to the process
            # TODO: Check balance (saldo)
            
            db_item = models.ItemContrato(**item.model_dump(), id_contrato=db_contrato.id)
            db.add(db_item)
            
            # Simple calc for total
            total_contrato += (item.quantidade_contratada * item.valor_unitario_final)
        
        db_contrato.valor_total = total_contrato
        db.commit()
        db.refresh(db_contrato)
        
    except Exception as e:
        db.rollback()
        # In a real scenario, we might want to delete the contract if items fail, or ensure atomic transaction better
        raise HTTPException(status_code=400, detail=f"Error creating contract items: {str(e)}")

    return db_contrato

@router.get("/contratos/", response_model=List[schemas.Contrato])
def read_contratos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Contrato).offset(skip).limit(limit).all()

# --- AOCS ---
@router.post("/aocs/", response_model=schemas.AOCS)
def create_aocs(aocs: schemas.AOCSCreate, db: Session = Depends(get_db)):
    db_aocs = models.Aocs(**aocs.model_dump())
    db.add(db_aocs)
    db.commit()
    db.refresh(db_aocs)
    return db_aocs

@router.get("/aocs/", response_model=List[schemas.AOCS])
def read_aocs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Aocs).offset(skip).limit(limit).all()
