from app.repositories.base import BaseRepository
from app.models.gestao.aocs import AOCS

class AOCSRepository(BaseRepository[AOCS]):
    def __init__(self):
        super().__init__(AOCS)
