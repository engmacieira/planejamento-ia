from app.repositories.base import BaseRepository
from app.models.gestao.item_contrato import ItemContrato

class ItemContratoRepository(BaseRepository[ItemContrato]):
    def __init__(self):
        super().__init__(ItemContrato)
