import pytest
from app.models.core.log_auditoria_model import LogAuditoria

# Marca o arquivo todo para rodar com asyncio
pytestmark = pytest.mark.asyncio

async def test_create_log_auditoria(db_session):
    """
    Testa a criação de um log de auditoria simples.
    """
    novo_log = LogAuditoria(
        usuario_id=None, # Ação do sistema
        acao="CREATE",
        entidade="Contrato",
        entidade_id="100",
        ip_address="127.0.0.1"
    )
    
    db_session.add(novo_log)
    await db_session.commit()
    await db_session.refresh(novo_log)

    assert novo_log.id is not None
    assert novo_log.acao == "CREATE"
    assert novo_log.created_at is not None

async def test_log_json_storage(db_session):
    """
    Testa se o banco consegue armazenar e recuperar dicionários JSON nos campos de snapshot.
    Isso é vital para o recurso de 'Ver Histórico de Alterações'.
    """
    snapshot_anterior = {"valor": 1000, "status": "Rascunho"}
    snapshot_novo = {"valor": 1000, "status": "Ativo"}

    log = LogAuditoria(
        acao="UPDATE",
        entidade="Contrato",
        dados_anteriores=snapshot_anterior,
        dados_novos=snapshot_novo
    )
    
    db_session.add(log)
    await db_session.commit()
    await db_session.refresh(log)

    # Verifica se recuperou como dict (Python) e se os valores batem
    assert log.dados_anteriores["status"] == "Rascunho"
    assert log.dados_novos["status"] == "Ativo"
    assert isinstance(log.dados_novos, dict)