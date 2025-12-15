from sqlalchemy.orm import Session
from app.repositories.licitacao.modalidade import ModalidadeRepository
from app.schemas.licitacao import ModalidadeBase

class ModalidadeService:
    def __init__(self):
        self.modalidade_repo = ModalidadeRepository()

    def get_modalidades(self, db: Session, skip: int = 0, limit: int = 100):
        return self.modalidade_repo.get_all(db, skip, limit)

    def create_modalidade(self, db: Session, modalidade_in: ModalidadeBase):
        return self.modalidade_repo.create(db, modalidade_in.model_dump())
