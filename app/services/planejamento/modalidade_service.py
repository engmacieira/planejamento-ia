from sqlalchemy.orm import Session
from app.repositories.gestao.modalidade_repository import ModalidadeRepository
from app.schemas.gestao.modalidade_schema import ModalidadeBase 

class ModalidadeService:
    def get_modalidades(self, db: Session, skip: int = 0, limit: int = 100):
        repo = ModalidadeRepository(db)
        return repo.get_all(skip, limit)

    def create_modalidade(self, db: Session, modalidade_in: ModalidadeBase):
        repo = ModalidadeRepository(db)
        return repo.create(modalidade_in)
