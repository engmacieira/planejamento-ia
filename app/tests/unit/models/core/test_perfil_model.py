import pytest
from sqlalchemy.exc import IntegrityError
from app.models.core.perfil_model import Perfil

# Marca o arquivo todo para rodar com asyncio
pytestmark = pytest.mark.asyncio

async def test_create_perfil_com_permissoes(db_session):
    """
    Testa a criação de um perfil com estrutura complexa de permissões (JSON).
    Isso simula a integração com o sistema de segurança do Core.
    """
    regras_gestor = {
        "scopes": ["dashboard:view", "pedido:approve"],
        "limite_alcada": 10000.00
    }

    novo_perfil = Perfil(
        nome="Gestor Financeiro",
        descricao="Aprova pedidos até 10k",
        permissoes=regras_gestor,
        ativo=True
    )
    
    db_session.add(novo_perfil)
    await db_session.commit()
    await db_session.refresh(novo_perfil)

    assert novo_perfil.id is not None
    assert novo_perfil.permissoes["scopes"][1] == "pedido:approve"
    assert novo_perfil.permissoes["limite_alcada"] == 10000.00

async def test_perfil_nome_unico(db_session):
    """
    Garante que não existam dois perfis com o mesmo nome.
    """
    p1 = Perfil(nome="Admin")
    db_session.add(p1)
    await db_session.commit()

    p2 = Perfil(nome="Admin") # Duplicado
    db_session.add(p2)

    with pytest.raises(IntegrityError):
        await db_session.commit()
    
    await db_session.rollback()

async def test_perfil_soft_delete(db_session):
    """
    Testa o ciclo de vida: Ativo -> Inativo -> Soft Deleted.
    """
    perfil = Perfil(nome="Temporario", ativo=True)
    db_session.add(perfil)
    await db_session.commit()

    # 1. Inativação de Negócio (Ainda existe, mas não atribui a novos users)
    perfil.ativo = False
    await db_session.commit()
    assert perfil.is_deleted is False

    # 2. Exclusão de Sistema (Foi para a lixeira)
    perfil.is_deleted = True
    await db_session.commit()
    
    await db_session.refresh(perfil)
    assert perfil.is_deleted is True