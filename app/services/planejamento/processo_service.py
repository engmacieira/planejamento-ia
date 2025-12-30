from sqlalchemy.orm import Session
from app.repositories.planejamento.processo_repository import ProcessoRepository
from app.repositories.planejamento.dfd_repository import DFDRepository
from app.schemas.planejamento.processo_schema import ProcessoCreate

class ProcessoService:
    def get_processos(self, db: Session, skip: int = 0, limit: int = 100):
        repo = ProcessoRepository(db)
        return repo.get_all(skip, limit)

    def get_processo(self, db: Session, processo_id: int):
        repo = ProcessoRepository(db)
        return repo.get_by_id(processo_id)

    def create_processo(self, db: Session, processo_in: ProcessoCreate):
        # Logic: Verify DFD exists
        dfd_repo = DFDRepository(db)
        db_dfd = dfd_repo.get_by_id(processo_in.id_dfd)
        if not db_dfd:
            raise ValueError("DFD not found")
            
        # Logic: Verify DFD usage
        if db_dfd.processo:
             raise ValueError("DFD already linked to a process")

        repo = ProcessoRepository(db)
        return repo.create(processo_in)
