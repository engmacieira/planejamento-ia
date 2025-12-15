from app.repositories.base import BaseRepository
from app.models.licitacao import DFD

class DFDRepository(BaseRepository[DFD]):
    def __init__(self):
        super().__init__(DFD)
