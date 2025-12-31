import pytest
from sqlalchemy.exc import IntegrityError
from app.models.core.agente_model import Agente

# Marca o arquivo todo para rodar com asyncio
pytestmark = pytest.mark.asyncio

async def test_create_agente(db_session):
    """
    Testa a criação de um Agente com todos os campos.
    """
    novo_agente = Agente(
        nome="João da Silva",
        cpf="12345678900",
        email="joao@teste.com",
        telefone="11999999999",
        matricula="12345",
        cargo="Fiscal de Contrato",
        ativo=True
    )
    
    db_session.add(novo_agente)
    await db_session.commit()
    await db_session.refresh(novo_agente)

    assert novo_agente.id is not None
    assert novo_agente.nome == "João da Silva"
    assert novo_agente.created_at is not None  # Valida herança do DefaultModel
    assert novo_agente.is_deleted is False     # Valida Soft Delete padrão

async def test_agente_cpf_unique(db_session):
    """
    Garante que não é possível criar dois agentes com o mesmo CPF.
    """
    agente1 = Agente(nome="Agente 1", cpf="11111111111")
    db_session.add(agente1)
    await db_session.commit()

    agente2 = Agente(nome="Agente 2", cpf="11111111111") # CPF Duplicado
    db_session.add(agente2)

    with pytest.raises(IntegrityError):
        await db_session.commit()
    
    await db_session.rollback()

async def test_agente_business_status(db_session):
    """
    Testa a diferença entre 'ativo' (negócio) e 'is_deleted' (sistema).
    Um agente pode estar inativo (aposentado) mas existir no sistema.
    """
    agente = Agente(
        nome="Agente Aposentado",
        cpf="22222222222",
        ativo=False  # Inativo no negócio
    )
    db_session.add(agente)
    await db_session.commit()

    assert agente.ativo is False
    assert agente.is_deleted is False # Ainda existe no banco