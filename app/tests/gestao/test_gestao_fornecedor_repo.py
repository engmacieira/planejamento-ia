import pytest
from app.repositories.gestao.fornecedor_repository import FornecedorRepository
from app.schemas.gestao.fornecedor_schema import FornecedorRequest

@pytest.mark.asyncio
async def test_create_fornecedor_success(db_session):
    repo = FornecedorRepository(db_session)
    data = FornecedorRequest(
        razao_social="Empresa Teste LTDA",
        nome_fantasia="Teste Tech",
        cpf_cnpj="12345678000199",
        email="contato@teste.com",
        telefone="1199999999"
    )
    
    result = await repo.create(data)
    
    assert result.id is not None
    assert result.razao_social == "Empresa Teste LTDA"
    assert result.cpf_cnpj == "12345678000199"

@pytest.mark.asyncio
async def test_get_fornecedor_by_cpf_cnpj(db_session):
    repo = FornecedorRepository(db_session)
    data = FornecedorRequest(
        razao_social="Busca por CPF",
        cpf_cnpj="98765432100",
        email="busca@teste.com"
    )
    created = await repo.create(data)
    
    found = await repo.get_by_cpf_cnpj("98765432100")
    assert found is not None
    assert found.id == created.id
    assert found.razao_social == "Busca por CPF"
    
    not_found = await repo.get_by_cpf_cnpj("00000000000")
    assert not_found is None
