import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.pool import StaticPool
from datetime import date

from httpx import AsyncClient, ASGITransport

# --- IMPORTS DA APLICAÇÃO ---
from app.main import app 
from app.core.database import Base
# Importamos o MÓDULO database para fazer o patch da engine
from app.core import database as real_database_module 

from app.core.deps import get_db, get_current_user, get_current_active_superuser, oauth2_scheme
from app.core.security import create_access_token, get_password_hash

# --- MODELS ---
from app.models.core.user_model import User
from app.models.core.unidade_model import Unidade
from app.models.gestao.fornecedor_model import Fornecedor
from app.models.planejamento.categoria_model import Categoria
from app.models.gestao.instrumento_model import InstrumentoContratual
from app.models.planejamento.modalidade_model import Modalidade
from app.models.planejamento.dfd_model import DFD
from app.models.planejamento.processo_licitatorio_model import ProcessoLicitatorio
from app.models.gestao.catalogo_item_model import CatalogoItem
from app.models.planejamento.grupo_model import Grupo
from app.models.planejamento.subgrupo_model import Subgrupo

# --- CONFIGURAÇÃO DO BANCO EM MEMÓRIA ---
# check_same_thread=False é crucial para testes async com SQLite
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=test_engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# --- CLASS MOCK DE USUÁRIO ---
class UserMock:
    def __init__(self, id=1, username="usuario_teste", email="teste@teste.com"):
        self.id = id
        self.username = username
        self.email = email
        self.nome_completo = "Usuario Teste Mock"
        self.ativo = True
        self.is_active = True
        self.id_perfil = 1 # Admin
        self.nivel_acesso = 2

# --- FIXTURE DO BANCO DE DADOS ---
@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Cria as tabelas no banco em memória e entrega uma sessão.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# --- CLIENT PRINCIPAL (AQUI ESTAVA O PROBLEMA) ---
@pytest.fixture(scope="function")
async def client(db_session):
    """
    Cliente HTTP blindado.
    Faz o patch da engine real para evitar conexões externas e
    faz o bypass da autenticação.
    """
    # 1. PATCH NA ENGINE REAL DO APP (Solução do Travamento)
    # Isso engana o app.main para ele usar nosso banco em memória
    # mesmo que ele tente conectar no banco real no startup.
    real_database_module.engine = test_engine
    real_database_module.AsyncSessionLocal = TestingSessionLocal

    # 2. OVERRIDES DE DEPENDÊNCIA
    async def override_get_db():
        yield db_session

    def override_get_current_user():
        return UserMock()

    # Importante: Aceitar *args, **kwargs para não quebrar a assinatura
    def override_oauth2_scheme(*args, **kwargs):
        return "token_fake_bypass"

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_current_active_superuser] = override_get_current_user
    app.dependency_overrides[oauth2_scheme] = override_oauth2_scheme
    
    headers = {"Authorization": "Bearer token_falso_para_testes"}
    
    # 3. CRIAÇÃO DO CLIENTE
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test",
        headers=headers
    ) as c:
        yield c
    
    # 4. LIMPEZA
    app.dependency_overrides.clear()

# --- DEMAIS FIXTURES (Mantidas iguais) ---
# Copiei as mesmas fixtures da sua versão anterior para garantir compatibilidade

@pytest.fixture(scope="function")
async def sample_user(db_session):
    stmt = select(User).where(User.username == "usuario_teste")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    password_hash = get_password_hash("123456")
    user = User(
        username="usuario_teste",
        email="teste@teste.com",
        nome_completo="Usuario Teste",
        password_hash=password_hash,
        ativo=True,
        cpf="00011122233", 
        telefone="11999999999",
        id_perfil=1 
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
async def usuario_normal_token(sample_user):
    access_token = create_access_token(data={"sub": str(sample_user.id)})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function")
async def sample_unidade(db_session):
    stmt = select(Unidade).where(Unidade.nome == "Unidade Teste")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    unidade = Unidade(
        codigo_administrativo="001",
        nome="Unidade Teste", 
        sigla="UT",
        ativo=True
    )
    db_session.add(unidade)
    await db_session.commit()
    await db_session.refresh(unidade)
    return unidade

@pytest.fixture(scope="function")
async def sample_fornecedor(db_session):
    fornecedor = Fornecedor(
        razao_social="Fornecedor Teste Ltda",
        cpf_cnpj="12345678000199",
        email="contato@fornecedor.com",
        telefone="11999999999"
    )
    db_session.add(fornecedor)
    await db_session.commit()
    await db_session.refresh(fornecedor)
    return fornecedor

@pytest.fixture(scope="function")
async def sample_categoria(db_session):
    stmt = select(Categoria).where(Categoria.nome == "Serviços")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    cat = Categoria(nome="Serviços", codigo_taxonomia="SV", ativo=True)
    db_session.add(cat)
    await db_session.commit()
    return cat

@pytest.fixture(scope="function")
async def sample_instrumento(db_session):
    stmt = select(InstrumentoContratual).where(InstrumentoContratual.nome == "Contrato")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    inst = InstrumentoContratual(nome="Contrato", ativo=True)
    db_session.add(inst)
    await db_session.commit()
    return inst

@pytest.fixture(scope="function")
async def sample_modalidade(db_session):
    stmt = select(Modalidade).where(Modalidade.nome == "Pregão Eletrônico")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    mod = Modalidade(nome="Pregão Eletrônico", ativo=True)
    db_session.add(mod)
    await db_session.commit()
    return mod

@pytest.fixture(scope="function")
async def sample_dfd(db_session, sample_unidade, sample_user):
    dfd = DFD(
        numero=1,
        ano=2024,
        descricao_sucinta="DFD Teste",
        unidade_requisitante_id=sample_unidade.id,
        responsavel_id=sample_user.id,
        data_req=date.today(),
        status="Rascunho",
        is_active=True
    )
    db_session.add(dfd)
    await db_session.commit()
    await db_session.refresh(dfd)
    return dfd

@pytest.fixture(scope="function")
async def sample_processo(db_session, sample_dfd, sample_modalidade):
    stmt = select(ProcessoLicitatorio).where(ProcessoLicitatorio.numero_processo == 1)
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    processo = ProcessoLicitatorio(
        id_dfd=sample_dfd.id,
        numero_processo=1,
        ano_processo=2024,
        id_modalidade=sample_modalidade.id,
        objeto="Processo Licitatório de Teste",
        status="Concluído"
    )
    db_session.add(processo)
    await db_session.commit()
    await db_session.refresh(processo)
    return processo

@pytest.fixture(scope="function")
async def sample_grupo(db_session, sample_categoria):
    stmt = select(Grupo).where(Grupo.codigo == "33")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    grupo = Grupo(
        categoria_id=sample_categoria.id,
        codigo="33", 
        nome="Despesas Correntes",
        ativo=True
    )
    db_session.add(grupo)
    await db_session.commit()
    await db_session.refresh(grupo)
    return grupo

@pytest.fixture(scope="function")
async def sample_subgrupo(db_session, sample_grupo):
    stmt = select(Subgrupo).where(Subgrupo.codigo == "90")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    subgrupo = Subgrupo(
        grupo_id=sample_grupo.id,
        codigo="90",
        nome="Aplicações Diretas",
        ativo=True
    )
    db_session.add(subgrupo)
    await db_session.commit()
    await db_session.refresh(subgrupo)
    return subgrupo

@pytest.fixture(scope="function")
async def sample_catalogo_item(db_session, sample_subgrupo):
    stmt = select(CatalogoItem).where(CatalogoItem.codigo_identificacao_completo == "1001")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    item = CatalogoItem(
        id_subgrupo=sample_subgrupo.id,
        nome_item="Item de Catálogo Teste",
        unidade_medida="UN",
        tipo="Material",
        numero_sequencial_taxonomia="0001",
        codigo_identificacao_completo="1001",
        ativo=True
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)
    return item