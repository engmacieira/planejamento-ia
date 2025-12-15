from app.repositories.base import BaseRepository
from app.models import Contrato

class ContratoRepository(BaseRepository[Contrato]):
    def __init__(self):
        super().__init__(Contrato)
