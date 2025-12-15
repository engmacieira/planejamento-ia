from app.repositories.base import BaseRepository
from app.models.gestao.contrato import Contrato

class ContratoRepository(BaseRepository[Contrato]):
    def __init__(self):
        super().__init__(Contrato)
