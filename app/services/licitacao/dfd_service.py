from sqlalchemy.orm import Session
from app.repositories.licitacao.dfd import DFDRepository
from app.repositories.licitacao.item_dfd import ItemDFDRepository
from app.schemas.licitacao import DFDCreate, ItemDFDCreate, AFDUpdate
from app.models.licitacao import DFD, ItemDFD

class DFDService:
    def __init__(self):
        self.dfd_repo = DFDRepository()
        self.item_dfd_repo = ItemDFDRepository()

    def get_dfds(self, db: Session, skip: int = 0, limit: int = 100):
        return self.dfd_repo.get_all(db, skip, limit)

    def get_dfd(self, db: Session, dfd_id: int):
        return self.dfd_repo.get(db, dfd_id)

    def create_dfd(self, db: Session, dfd_in: DFDCreate):
        return self.dfd_repo.create(db, dfd_in.model_dump())

    def update_status(self, db: Session, dfd_id: int, status_update: AFDUpdate):
        db_dfd = self.dfd_repo.get(db, dfd_id)
        if not db_dfd:
            return None
        return self.dfd_repo.update(db, db_dfd, {"status": status_update.status})

    def add_item(self, db: Session, dfd_id: int, item_in: ItemDFDCreate):
        # Business Logic: Check if DFD exists
        db_dfd = self.dfd_repo.get(db, dfd_id)
        if not db_dfd:
            return None # Or raise specific Exception handled by router
        
        # TODO: Check Catalog
        
        item_data = item_in.model_dump()
        item_data['id_dfd'] = dfd_id
        return self.item_dfd_repo.create(db, item_data)
