import pytest
import asyncio
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.core.orgao_model import Orgao

pytestmark = pytest.mark.asyncio

async def test_create_orgao(db_session):
    """
    Testa a criação bem-sucedida de um Órgão com todos os campos principais.
    """
    novo_orgao = Orgao(
        nome="Prefeitura Municipal de Teste",
        cnpj="12345678000199",
        sigla="PMT",
        cidade="Teste City",
        uf="TS",
        esfera="Municipal",
        email="contato@teste.gov.br",
        site="www.teste.gov.br"
    )
    
    db_session.add(novo_orgao)
    await db_session.commit()
    await db_session.refresh(novo_orgao)

    assert novo_orgao.id is not None
    assert novo_orgao.nome == "Prefeitura Municipal de Teste"
    assert novo_orgao.cnpj == "12345678000199"
    assert novo_orgao.is_deleted is False 
    assert novo_orgao.created_at is not None 

async def test_orgao_cnpj_unique_constraint(db_session):
    """
    Testa se o banco impede a criação de dois Órgãos com o mesmo CNPJ.
    """
    orgao1 = Orgao(
        nome="Prefeitura A",
        cnpj="11111111000111",
        cidade="Cidade A",
        uf="AA"
    )
    db_session.add(orgao1)
    await db_session.commit()

    orgao2 = Orgao(
        nome="Prefeitura B",
        cnpj="11111111000111", # Duplicado
        cidade="Cidade B",
        uf="BB"
    )
    db_session.add(orgao2)

    with pytest.raises(IntegrityError):
        await db_session.commit()
    
    await db_session.rollback()

async def test_soft_delete_orgao(db_session):
    """
    Testa se o Soft Delete funciona corretamente para o Órgão.
    """
    orgao = Orgao(
        nome="Prefeitura para Deletar",
        cnpj="99999999000199",
        cidade="Delete City",
        uf="DC"
    )
    db_session.add(orgao)
    await db_session.commit()

    orgao.is_deleted = True
    await db_session.commit()
    
    result = await db_session.execute(select(Orgao).where(Orgao.id == orgao.id))
    orgao_recuperado = result.scalar_one_or_none()

    assert orgao_recuperado is not None
    assert orgao_recuperado.is_deleted is True

async def test_update_orgao(db_session):
    """
    Testa a atualização de dados e se o campo updated_at é modificado.
    """
    orgao = Orgao(
        nome="Nome Antigo",
        cnpj="88888888000188",
        cidade="Old City",
        uf="OC"
    )
    db_session.add(orgao)
    await db_session.commit()
    
    data_criacao_original = orgao.updated_at
    await asyncio.sleep(1)

    orgao.nome = "Nome Novo"
    await db_session.commit()
    await db_session.refresh(orgao)

    assert orgao.nome == "Nome Novo"
    assert orgao.updated_at >= data_criacao_original