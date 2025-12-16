import pytest
from app.repositories.planejamento.dfd_repository import DFDRepository
from app.schemas.planejamento.dfd_schema import DFDCreate
from app.models.planejamento.dfd_model import DFD

@pytest.mark.asyncio
async def test_create_dfd_complete(db_session, sample_unidade):
    # DFD requires a Unit. sample_unidade fixture provides one.
    # Assuming db_session and sample_unidade are compatible with Async
    
    repo = DFDRepository(db_session)
    
    # Prepare DFD Data
    dfd_data = DFDCreate(
        numero=123,
        ano=2024,
        # Schema requires these fields now:
        data_req="2024-03-15",
        unidade_requisitante_id=sample_unidade.id, # Using direct field, not alias
        responsavel_id=1, # Mock ID
        objeto="Aquisição de Computadores",
        justificativa="Modernização do parque tecnológico",
        # Base fields mapped:
        numero_protocolo_string="123/2024",
        contratacao_vinculada=False,
        itens=[],
        equipe=[],
        dotacoes=[]
    )
    
    # Create DFD
    created_dfd = await repo.create(dfd_data)
    
    # Assertions
    assert created_dfd.id is not None
    assert created_dfd.numero == 123
    assert created_dfd.descricao_sucinta == "Aquisição de Computadores"
    assert created_dfd.unidade_requisitante_id == sample_unidade.id

@pytest.mark.asyncio
async def test_get_dfd_by_id(db_session, sample_unidade):
    repo = DFDRepository(db_session)
    # Setup
    dfd = DFD(
        numero=456,
        ano=2024,
        descricao_sucinta="Teste Get",
        unidade_requisitante_id=sample_unidade.id,
        status="Rascunho",
        is_active=True
    )
    db_session.add(dfd)
    await db_session.commit()
    await db_session.refresh(dfd)
    
    # Execution
    retrieved = await repo.get_by_id(dfd.id)
    
    # Assertions
    assert retrieved is not None
    assert retrieved.id == dfd.id
    assert retrieved.descricao_sucinta == "Teste Get"
