from app.repositories.base import BaseRepository
from app.models.gestao.instrumento import InstrumentoContratual

class InstrumentoRepository(BaseRepository[InstrumentoContratual]):
    def __init__(self):
        super().__init__(InstrumentoContratual)
