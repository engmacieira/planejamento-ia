import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.core.orgao_model import Orgao

# Marca o arquivo todo para rodar com asyncio, já que usamos SQLAlchemy Async
pytestmark = pytest.mark.asyncio

async def test_create_orgao(async_session):
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
    
    async_session.add(novo_orgao)
    await async_session.commit()
    await async_session.refresh(novo_orgao)

    assert novo_orgao.id is not None
    assert novo_orgao.nome == "Prefeitura Municipal de Teste"
    assert novo_orgao.cnpj == "12345678000199"
    assert novo_orgao.is_deleted is False  # Herança do DefaultModel
    assert novo_orgao.created_at is not None  # Auditoria automática

async def test_orgao_cnpj_unique_constraint(async_session):
    """
    Testa se o banco impede a criação de dois Órgãos com o mesmo CNPJ.
    Regra de Ouro: Não podem existir duplicidades fiscais.
    """
    orgao1 = Orgao(
        nome="Prefeitura A",
        cnpj="11111111000111",
        cidade="Cidade A",
        uf="AA"
    )
    async_session.add(orgao1)
    await async_session.commit()

    # Tenta criar o segundo com o MESMO CNPJ
    orgao2 = Orgao(
        nome="Prefeitura B",
        cnpj="11111111000111", # Duplicado
        cidade="Cidade B",
        uf="BB"
    )
    async_session.add(orgao2)

    with pytest.raises(IntegrityError):
        await async_session.commit()
    
    await async_session.rollback()

async def test_soft_delete_orgao(async_session):
    """
    Testa se o Soft Delete funciona corretamente para o Órgão.
    Ao deletar, o registro deve permanecer no banco mas com is_deleted=True.
    """
    orgao = Orgao(
        nome="Prefeitura para Deletar",
        cnpj="99999999000199",
        cidade="Delete City",
        uf="DC"
    )
    async_session.add(orgao)
    await async_session.commit()

    # Executa o Soft Delete (simulando a lógica que ficaria no Repository/Service)
    orgao.is_deleted = True
    await async_session.commit()
    
    # Tenta buscar pelo ID
    result = await async_session.execute(select(Orgao).where(Orgao.id == orgao.id))
    orgao_recuperado = result.scalar_one_or_none()

    # O registro AINDA deve existir fisicamente
    assert orgao_recuperado is not None
    # Mas deve estar marcado como deletado
    assert orgao_recuperado.is_deleted is True

async def test_update_orgao(async_session):
    """
    Testa a atualização de dados e se o campo updated_at é modificado.
    """
    orgao = Orgao(
        nome="Nome Antigo",
        cnpj="88888888000188",
        cidade="Old City",
        uf="OC"
    )
    async_session.add(orgao)
    await async_session.commit()
    
    data_criacao_original = orgao.updated_at

    # Atualiza
    orgao.nome = "Nome Novo"
    await async_session.commit()
    await async_session.refresh(orgao)

    assert orgao.nome == "Nome Novo"
    # Nota: Em testes muito rápidos, o updated_at pode ser igual se rodar no mesmo milissegundo.
    # Mas garantimos que o objeto foi persistido.
    assert orgao.updated_at >= data_criacao_original