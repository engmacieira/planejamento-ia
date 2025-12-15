from sqlalchemy.orm import Session
from app.repositories.licitacao.processo import ProcessoRepository
from app.repositories.licitacao.dfd import DFDRepository
from app.schemas.licitacao import ProcessoLicitatorioCreate

class ProcessoService:
    def __init__(self):
        self.processo_repo = ProcessoRepository()
        self.dfd_repo = DFDRepository()

    def get_processos(self, db: Session, skip: int = 0, limit: int = 100):
        return self.processo_repo.get_all(db, skip, limit)

    def get_processo(self, db: Session, processo_id: int):
        return self.processo_repo.get(db, processo_id)

    def create_processo(self, db: Session, processo_in: ProcessoLicitatorioCreate):
        # Logic: Verify DFD exists
        db_dfd = self.dfd_repo.get(db, processo_in.id_dfd)
        if not db_dfd:
            raise ValueError("DFD not found")
            
        # Logic: Verify DFD usage
        if db_dfd.processo:
             raise ValueError("DFD already linked to a process")

        return self.processo_repo.create(db, processo_in.model_dump())
