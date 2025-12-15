from app.repositories.base import BaseRepository
from app.models import ItemContrato

class ItemContratoRepository(BaseRepository[ItemContrato]):
    def __init__(self):
        super().__init__(ItemContrato)
