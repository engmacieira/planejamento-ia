import pytest
from app.repositories.gestao.tipo_documento_repository import TipoDocumentoRepository
from app.schemas.gestao.tipo_documento_schema import TipoDocumentoRequest

@pytest.mark.asyncio
async def test_tipo_documento_crud(db_session):
    repo = TipoDocumentoRepository(db_session)
    
    tipo = await repo.get_or_create("PDF Assinado")
    assert tipo.id is not None
    assert tipo.nome == "PDF Assinado"
    
    tipo2 = await repo.get_or_create("PDF Assinado")
    assert tipo2.id == tipo.id
    
    tipo3 = await repo.get_or_create("Excel")
    assert tipo3.id != tipo.id
