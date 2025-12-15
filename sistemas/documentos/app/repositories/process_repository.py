from sqlalchemy.orm import Session
from app.models.process_model import Processo
from app.schemas.process_schema import ProcessoCreate

class ProcessoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, schema: ProcessoCreate, owner_id: int):
        db_processo = Processo(
            **schema.model_dump(), # Desempacota todos os campos do schema automaticamente
            owner_id=owner_id
        )
        self.db.add(db_processo)
        self.db.commit()
        self.db.refresh(db_processo)
        return db_processo

    def list_by_user(self, owner_id: int):
        return self.db.query(Processo).filter(Processo.owner_id == owner_id).all()
        
    def get_by_id(self, id: int):
        return self.db.query(Processo).filter(Processo.id == id).first()