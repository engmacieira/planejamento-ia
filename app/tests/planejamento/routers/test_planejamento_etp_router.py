import pytest
from app.repositories.planejamento.dfd_repository import DFDRepository
from app.schemas.planejamento.dfd_schema import DFDCreate, DFDItemBase

@pytest.mark.asyncio
async def test_etp_router_consolidar_and_lifecycle(client, usuario_normal_token, db_session, sample_unidade):
    # Setup DFDs
    repo = DFDRepository(db_session)
    dfd1 = await repo.create(DFDCreate(ano=2024, id_unidade_requisitante=sample_unidade.id, objeto="Obj1", justificativa="J"))
    dfd2 = await repo.create(DFDCreate(ano=2024, id_unidade_requisitante=sample_unidade.id, objeto="Obj2", justificativa="J"))
    
    # Consolidate
    pl = {"dfd_ids": [dfd1.id, dfd2.id]}
    r = await client.post("/etps/consolidar", json=pl, headers=usuario_normal_token)
    assert r.status_code == 201
    etp_id = r.json()["id"]
    
    # Get by DFD
    r = await client.get(f"/etps/dfd/{dfd1.id}", headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["id"] == etp_id
    
    # Update ETP
    r = await client.put(f"/etps/{etp_id}", json={"descricao_solucao": "Solucao Test"}, headers=usuario_normal_token)
    assert r.status_code == 200
    assert r.json()["descricao_solucao"] == "Solucao Test"
    
    # Unlink DFD1
    r = await client.delete(f"/etps/{etp_id}/unlink/{dfd1.id}", headers=usuario_normal_token)
    assert r.status_code == 200
    
    # Delete ETP (should free DFD2)
    r = await client.delete(f"/etps/{etp_id}", headers=usuario_normal_token)
    assert r.status_code == 200
