import pytest
from app.models.user_model import User
from app.schemas.process_schema import ProcessoCreate
from app.repositories.process_repository import ProcessoRepository

@pytest.fixture
def owner(db_session):
    user = User(name="Dono", email="dono@processo.com", password_hash="123")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_process_lifecycle(db_session, owner):
    """Testa Criar, Listar e Buscar por ID."""
    repo = ProcessoRepository(db_session)
    
    # 1. Criar
    data = ProcessoCreate(
        numero_dfd="001/2025",
        secretaria="Saúde",
        objeto="Remédios",
        valor_estimado="R$ 100,00",
        valor_extenso="cem reais",
        data1="10/10/2025"
    )
    
    processo = repo.create(data, owner.id)
    
    assert processo.id is not None
    assert processo.numero_dfd == "001/2025"
    assert processo.owner_id == owner.id

    # 2. Listar
    lista = repo.list_by_user(owner.id)
    assert len(lista) == 1
    assert lista[0].objeto == "Remédios"

    # 3. Get By ID
    buscado = repo.get_by_id(processo.id)
    assert buscado.secretaria == "Saúde"
    
    # 4. Get By ID Inexistente
    assert repo.get_by_id(999) is None