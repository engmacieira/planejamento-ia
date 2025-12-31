import pytest
from app.models.core.user_model import User
from app.models.core.unidade_model import Unidade
# Precisamos importar o modelo da tabela de junção para o SQLAlchemy registrar
from app.models.core.usuario_unidade_model import UsuarioUnidade 

pytestmark = pytest.mark.asyncio

async def test_create_user_multiplas_unidades(db_session):
    """
    Testa a funcionalidade de vincular um usuário a múltiplas secretarias (N:N).
    """
    # 1. Cria as Unidades
    saude = Unidade(nome="Secretaria de Saúde", sigla="SMS")
    educacao = Unidade(nome="Secretaria de Educação", sigla="SEMED")
    db_session.add_all([saude, educacao])
    await db_session.commit()

    # 2. Cria o Usuário
    joao = User(
        username="joao.multitask",
        email="joao@gov.br",
        password_hash="123",
        nome_completo="Joao da Silva",
        is_active=True
    )
    
    # 3. Faz o Vínculo (Mágica do SQLAlchemy)
    # Basta adicionar os objetos à lista 'unidades' do usuário
    joao.unidades.append(saude)
    joao.unidades.append(educacao)
    
    db_session.add(joao)
    await db_session.commit()
    
    # 4. Verifica
    # Recarrega do banco para garantir que persistiu
    await db_session.refresh(joao, attribute_names=["unidades"])
    
    assert len(joao.unidades) == 2
    assert joao.unidades[0].nome in ["Secretaria de Saúde", "Secretaria de Educação"]
    assert joao.unidades[1].nome in ["Secretaria de Saúde", "Secretaria de Educação"]

async def test_user_ativo_inativo(db_session):
    """
    Testa a flag de negócio 'is_active'.
    """
    user = User(
        username="user_ferias", 
        email="ferias@gov.br", 
        password_hash="123", 
        nome_completo="User Ferias",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()

    # Bloqueia login (ex: saiu de férias)
    user.is_active = False
    await db_session.commit()

    assert user.is_active is False
    assert user.is_deleted is False # Ainda existe no banco