import pytest
from app.repositories.planejamento.tr_repository import TRRepository
from app.repositories.planejamento.risk_repository import RiskRepository
from app.models.planejamento.etp_model import ETP

@pytest.mark.asyncio
async def test_tr_flow(db_session):
    risk_repo = RiskRepository(db_session)
    tr_repo = TRRepository(db_session)
    
    # Create ETP and Matriz
    etp = ETP(descricao_necessidade="For TR", viabilidade=True)
    db_session.add(etp)
    await db_session.commit()
    await db_session.refresh(etp)
    
    # Ensure Matriz exists (TR depends on it)
    await risk_repo.get_by_etp(etp.id)
    
    # Get TR (Auto Create)
    tr = await tr_repo.get_by_etp(etp.id)
    assert tr is not None
    assert tr.matriz_id is not None
    
    # Update
    updated = await tr_repo.update(tr.id, {"definicao_objeto": "Objeto TR"})
    assert updated.definicao_objeto == "Objeto TR"
