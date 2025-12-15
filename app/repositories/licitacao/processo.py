from app.repositories.base import BaseRepository
from app.models import ProcessoLicitatorio

class ProcessoRepository(BaseRepository[ProcessoLicitatorio]):
    def __init__(self):
        super().__init__(ProcessoLicitatorio)
