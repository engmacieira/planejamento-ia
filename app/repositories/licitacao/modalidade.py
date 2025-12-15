from app.repositories.base import BaseRepository
from app.models.licitacao import Modalidade

class ModalidadeRepository(BaseRepository[Modalidade]):
    def __init__(self):
        super().__init__(Modalidade)
