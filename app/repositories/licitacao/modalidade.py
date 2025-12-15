from app.repositories.base import BaseRepository
from app.models import Modalidade

class ModalidadeRepository(BaseRepository[Modalidade]):
    def __init__(self):
        super().__init__(Modalidade)
