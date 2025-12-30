from sqlalchemy.orm import Session
from app.repositories.planejamento.dfd_repository import DFDRepository
# from app.repositories.planejamento.item_dfd_repository import ItemDFDRepository # TODO: Locate or create ItemDFDRepository
from app.schemas.planejamento.dfd_schema import DFDCreate, DFDUpdate
# from app.schemas.planejamento.item_dfd_schema import ItemDFDCreate # TODO: Verify schema location
from app.models.planejamento.dfd_model import DFD
# from app.models.planejamento.item_dfd_model import ItemDFD

class DFDService:
    # Service methods adapted to instantiate Repository with the provided 'db' session
    # because the Repository now requires session in __init__.

    def get_dfds(self, db: Session, skip: int = 0, limit: int = 100):
        repo = DFDRepository(db)
        return repo.get_all(skip, limit)

    def get_dfd(self, db: Session, dfd_id: int):
        repo = DFDRepository(db)
        return repo.get_by_id(dfd_id)

    def create_dfd(self, db: Session, dfd_in: DFDCreate):
        repo = DFDRepository(db)
        return repo.create(dfd_in)

    def update_status(self, db: Session, dfd_id: int, status_update: DFDUpdate):
        repo = DFDRepository(db)
        # Assuming update method can handle status update via dict or schema, repo signature says 'dfd_data: dict'
        return repo.update(dfd_id, {"status": status_update.status}) # Check if status is in DFDUpdate or if we need a specific schema

    # def add_item(self, db: Session, dfd_id: int, item_in: ItemDFDCreate):
    #     # TODO: Restore this method when ItemDFDRepository is available
    #     # item_dfd_repo = ItemDFDRepository(db)
    #     
    #     # Business Logic: Check if DFD exists
    #     repo = DFDRepository(db)
    #     db_dfd = repo.get_by_id(dfd_id)
    #     if not db_dfd:
    #         return None 
    #     
    #     item_data = item_in.model_dump()
    #     item_data['id_dfd'] = dfd_id
    #     return item_dfd_repo.create(item_data)
