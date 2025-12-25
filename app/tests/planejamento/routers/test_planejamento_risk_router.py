import pytest
from unittest.mock import patch
from app.models.planejamento.etp_model import ETP

@pytest.mark.asyncio
async def test_risk_router_generate_mocked(client, usuario_normal_token):
    # Mock ai_service in risk_router
    with patch("app.routers.planejamento.risk_router.ai_service") as mock_service:
        # Mock returns string JSON
        mock_service.generate_risks.return_value = '[{"descricao_risco": "R1", "probabilidade": "Alta"}]'
        
        pl = {"etp_object": "Obj"}
        r = await client.post("/riscos/generate", json=pl, headers=usuario_normal_token)
        assert r.status_code == 200
        assert isinstance(r.json(), list)
        assert r.json()[0]["descricao_risco"] == "R1"

@pytest.mark.asyncio
async def test_risk_router_crud(client, usuario_normal_token, db_session):
    # Setup ETP
    etp = ETP(descricao_necessidade="Risk Test", viabilidade=True)
    db_session.add(etp)
    await db_session.commit()
    await db_session.refresh(etp)
    
    # Get Matriz (Auto-Create)
    r = await client.get(f"/riscos/etp/{etp.id}", headers=usuario_normal_token)
    assert r.status_code == 200
    matriz_id = r.json()["id"]
    
    # Add Risk
    risk_pl = {
        "descricao_risco": "Risco Manual",
        "probabilidade": "Baixa",
        "impacto": "Baixo",
        "medida_preventiva": "Prev",
        "responsavel": "Gestor"
    }
    r = await client.post(f"/riscos/item/{matriz_id}", json=risk_pl, headers=usuario_normal_token)
    assert r.status_code == 200
    risk_id = r.json()["id"]
    
    # Delete Risk
    r = await client.delete(f"/riscos/item/{risk_id}", headers=usuario_normal_token)
    assert r.status_code == 200
