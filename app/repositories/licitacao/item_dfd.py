from app.repositories.base import BaseRepository
from app.models.licitacao import ItemDFD

class ItemDFDRepository(BaseRepository[ItemDFD]):
    def __init__(self):
        super().__init__(ItemDFD)
