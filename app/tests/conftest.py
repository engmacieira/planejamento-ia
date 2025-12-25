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
# Importamos as dependências para fazer o OVERRIDE
from app.core.deps import get_db, get_current_user, get_current_active_superuser
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

# --- CONFIGURAÇÃO DO BANCO (SQLite Async em Memória) ---
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# --- CLASS MOCK DE USUÁRIO (O Impostor Honesto) ---
class UserMock:
    """
    Simula um objeto User para passar pelas dependências de segurança.
    Agora limpo: sem 'is_superuser' pois corrigimos a dependência.
    """
    def __init__(self, id=1, username="usuario_teste", email="teste@teste.com"):
        self.id = id
        self.username = username
        self.email = email
        self.nome_completo = "Usuario Teste Mock"
        self.ativo = True      # Campo real do banco
        self.is_active = True  # Property do model
        
        self.id_perfil = 1     # 1 = Admin (Isso satisfaz o deps.py corrigido)
        self.nivel_acesso = 2  # Nível de acesso legado, se usado

@pytest.fixture(scope="session")
def event_loop():
    """Cria uma instância do event loop para a sessão de testes."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Sessão de banco limpa para cada teste."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(db_session):
    """
    Cliente HTTP com autenticação ignorada (Bypass).
    """
    # 1. Override do Banco
    async def override_get_db():
        yield db_session

    # 2. Override da Auth (Bypass total)
    def override_get_current_user():
        return UserMock()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_current_active_superuser] = override_get_current_user
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()

# --- FIXTURES DE DADOS MESTRES ---

@pytest.fixture(scope="function")
async def sample_user(db_session):
    """
    Cria um usuário REAL no banco de dados.
    Corrigido: Sem campos inexistentes (is_superuser).
    """
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
        # Campos obrigatórios adicionados para evitar erros de Integridade
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
    """Gera token válido para testes que NÃO usam o override de auth."""
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

# --- FIXTURES HIERÁRQUICAS ---

@pytest.fixture(scope="function")
async def sample_categoria(db_session):
    stmt = select(Categoria).where(Categoria.nome == "Serviços")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    cat = Categoria(
        nome="Serviços", 
        codigo_taxonomia="SV",
        ativo=True
    )
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