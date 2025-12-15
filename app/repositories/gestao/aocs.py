from app.repositories.base import BaseRepository
from app.models import Aocs

class AOCSRepository(BaseRepository[Aocs]):
    def __init__(self):
        super().__init__(Aocs)
