from app.repositories.base import BaseRepository
from app.models.gestao.fornecedor import Fornecedor

class FornecedorRepository(BaseRepository[Fornecedor]):
    def __init__(self):
        super().__init__(Fornecedor)
