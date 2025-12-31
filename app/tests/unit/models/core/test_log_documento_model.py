import pytest
from app.models.core.log_documento_model import LogDocumento
from app.models.core.user_model import User

# Marca o arquivo todo para rodar com asyncio
pytestmark = pytest.mark.asyncio

async def test_create_log_ia(db_session):
    """
    Testa a criação de um log de geração com dados de IA.
    """
    # Precisamos de um usuário para vincular
    user = User(
        username="ia_tester", 
        email="ia@test.com", 
        password_hash="123", 
        nome_completo="IA Tester"
    )
    db_session.add(user)
    await db_session.commit()

    # Cria o Log
    log = LogDocumento(
        nome_arquivo_gerado="Minuta_Contrato_v1.docx",
        ia_model="gemini-1.5-pro",
        tokens_utilizados=1540,
        parametros_usados={"objeto": "Computadores", "valor": 50000},
        user_id=user.id
    )
    
    db_session.add(log)
    await db_session.commit()
    await db_session.refresh(log)

    assert log.id is not None
    assert log.ia_model == "gemini-1.5-pro"
    assert log.parametros_usados["objeto"] == "Computadores"
    assert log.user_id == user.id

async def test_log_relationship_user(db_session):
    """
    Testa se o relacionamento back_populates com User está funcionando.
    """
    user = User(
        username="log_user", 
        email="log@test.com", 
        password_hash="123", 
        nome_completo="Log User"
    )
    db_session.add(user)
    await db_session.commit()

    log = LogDocumento(
        nome_arquivo_gerado="Teste.pdf",
        user_id=user.id
    )
    db_session.add(log)
    await db_session.commit()

    # Traz o user e verifica se o log está na lista (lazy loading)
    await db_session.refresh(user, attribute_names=["logs"])
    assert len(user.logs) == 1
    assert user.logs[0].nome_arquivo_gerado == "Teste.pdf"