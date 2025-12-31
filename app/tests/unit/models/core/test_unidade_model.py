import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.core.unidade_model import Unidade

# Marca o arquivo todo para rodar com asyncio
pytestmark = pytest.mark.asyncio

async def test_create_unidade(db_session):
    """
    Testa a criação de uma Unidade ativa por padrão.
    """
    nova_unidade = Unidade(
        nome="Secretaria de Educação",
        sigla="SEMED",
        codigo_interno="EDU-001"
    )
    
    db_session.add(nova_unidade)
    await db_session.commit()
    await db_session.refresh(nova_unidade)

    assert nova_unidade.id is not None
    assert nova_unidade.ativo is True  # Default deve ser True
    assert nova_unidade.is_deleted is False

async def test_unidade_unique_name(db_session):
    """
    Garante que não existem duas secretarias com o mesmo nome exato.
    """
    u1 = Unidade(nome="Saúde")
    db_session.add(u1)
    await db_session.commit()

    u2 = Unidade(nome="Saúde") # Duplicado
    db_session.add(u2)

    with pytest.raises(IntegrityError):
        await db_session.commit()
    
    await db_session.rollback()

async def test_unidade_business_status(db_session):
    """
    Testa a diferença entre 'ativo' (negócio) e 'is_deleted' (sistema).
    Ex: Secretaria Extinta.
    """
    unidade_extinta = Unidade(
        nome="Secretaria Extraordinária da Copa",
        ativo=False # Não funciona mais
    )
    db_session.add(unidade_extinta)
    await db_session.commit()

    assert unidade_extinta.ativo is False
    assert unidade_extinta.is_deleted is False # Mas o registro existe!

    # Agora deletamos (Soft Delete)
    unidade_extinta.is_deleted = True
    await db_session.commit()
    
    # Busca no banco
    result = await db_session.execute(select(Unidade).where(Unidade.id == unidade_extinta.id))
    recuperado = result.scalar_one()
    
    assert recuperado.is_deleted is True