import pytest
from app.repositories.gestao.fornecedor_repository import FornecedorRepository
from app.schemas.gestao.fornecedor_schema import FornecedorRequest

@pytest.mark.asyncio
async def test_fornecedor_lifecycle(db_session):
    repo = FornecedorRepository(db_session)
    
    data = FornecedorRequest(
        razao_social="Tech Corp",
        cpf_cnpj="12345678901234",
        email="contact@tech.com",
        telefone="11987654321"
    )
    
    # Create
    fornecedor = await repo.create(data)
    assert fornecedor.id is not None
    assert fornecedor.cpf_cnpj == "12345678901234"
    
    # Get by CPF/CNPJ
    found = await repo.get_by_cpf_cnpj("12345678901234")
    assert found.id == fornecedor.id
    
    # Get or Create
    # 1. Existing by CPF/CNPJ
    f_goc = await repo.get_or_create(data)
    assert f_goc.id == fornecedor.id
    
    # 2. Existing by ID
    f_goc_id = await repo.get_or_create(None, id_fornecedor=fornecedor.id)
    assert f_goc_id.id == fornecedor.id
    
    # 3. New
    new_data = FornecedorRequest(razao_social="New Corp", cpf_cnpj="98765432109876")
    f_new = await repo.get_or_create(new_data)
    assert f_new.id != fornecedor.id
    assert f_new.cpf_cnpj == "98765432109876"
