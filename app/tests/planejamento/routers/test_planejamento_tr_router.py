import pytest
from unittest.mock import patch
from app.models.planejamento.etp_model import ETP
from app.repositories.planejamento.risk_repository import RiskRepository

@pytest.mark.asyncio
async def test_tr_router_generate_clause(client, usuario_normal_token, db_session):
    # Setup ETP
    etp = ETP(descricao_necessidade="TR Gen Test", viabilidade=True)
    db_session.add(etp)
    await db_session.commit()
    await db_session.refresh(etp)
    
    # Setup Matriz (Depends on logic inside router setup)
    await RiskRepository(db_session).get_by_etp(etp.id)
    
    with patch("app.routers.planejamento.tr_router.ai_service") as mock_service:
        mock_service.generate_tr_clause.return_value = "Clause Text"
        
        pl = {"etp_id": etp.id, "section": "obrigacoes"}
        r = await client.post("/trs/generate/clause", json=pl, headers=usuario_normal_token)
        assert r.status_code == 200
        assert r.json()["result"] == "Clause Text"

@pytest.mark.asyncio
async def test_tr_router_crud(client, usuario_normal_token, db_session):
    # Setup ETP & Matriz
    etp = ETP(descricao_necessidade="TR CRUD", viabilidade=True)
    db_session.add(etp)
    await db_session.commit()
    await db_session.refresh(etp)
    await RiskRepository(db_session).get_by_etp(etp.id)
    
    # Get TR (Auto-Create)
    r = await client.get(f"/trs/etp/{etp.id}", headers=usuario_normal_token)
    assert r.status_code == 200
    tr_id = r.json()["id"]
    
    # Update TR
    pl = {"definicao_objeto": "Objeto TR Updated"}
    r = await client.put(f"/trs/{tr_id}", json=pl, headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["definicao_objeto"] == "Objeto TR Updated"
