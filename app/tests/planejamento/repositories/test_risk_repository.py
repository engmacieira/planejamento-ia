import pytest
from app.repositories.planejamento.risk_repository import RiskRepository
from app.models.planejamento.etp_model import ETP

@pytest.mark.asyncio
async def test_risk_flow(db_session):
    repo = RiskRepository(db_session)
    
    # Create Dummy ETP manually for FK
    etp = ETP(descricao_necessidade="For Risk", viabilidade=True)
    db_session.add(etp)
    await db_session.commit()
    await db_session.refresh(etp)
    
    # Get (Auto Create)
    matriz = await repo.get_by_etp(etp.id)
    assert matriz is not None
    assert matriz.etp_id == etp.id
    
    # Add Risk
    risk_data = {
        "descricao_risco": "Risk 1",
        "probabilidade": "Alta",
        "impacto": "Alto",
        "acao_preventiva": "Action"
    }
    risco = await repo.add_risk(matriz.id, risk_data)
    assert risco.id is not None
    assert risco.descricao_risco == "Risk 1"
    
    # Delete Risk
    success = await repo.delete_risk(risco.id)
    assert success is True
