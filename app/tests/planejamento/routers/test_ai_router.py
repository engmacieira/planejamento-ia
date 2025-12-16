import pytest
from unittest.mock import MagicMock, patch

@pytest.mark.asyncio
async def test_ai_router_generate_object(client, usuario_normal_token):
    # Mock the ai_service instance in the router module
    with patch("app.routers.planejamento.ai_router.ai_service") as mock_service:
        mock_service.generate_dfd_object.return_value = "Mocked Object"
        
        pl = {"draft_text": "Rascunho", "user_instructions": ""}
        r = await client.post("/ai/generate/dfd-object", json=pl, headers=usuario_normal_token)
        
        assert r.status_code == 200
        assert r.json()["result"] == "Mocked Object"

@pytest.mark.asyncio
async def test_ai_router_generate_justification(client, usuario_normal_token):
    with patch("app.routers.planejamento.ai_router.ai_service") as mock_service:
        mock_service.generate_dfd_justification.return_value = "Mocked Justification"
        
        pl = {"object_text": "Obj", "draft_text": "", "user_instructions": ""}
        r = await client.post("/ai/generate/dfd-justification", json=pl, headers=usuario_normal_token)
        
        assert r.status_code == 200
        assert r.json()["result"] == "Mocked Justification"

# Add more tests for other AI endpoints following the same pattern if needed.
# Covering the critical path ensures connectivity.
