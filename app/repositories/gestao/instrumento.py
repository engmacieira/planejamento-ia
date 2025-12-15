from app.repositories.base import BaseRepository
from app.models import InstrumentoContratual

class InstrumentoRepository(BaseRepository[InstrumentoContratual]):
    def __init__(self):
        super().__init__(InstrumentoContratual)
