import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.pool import StaticPool # Essencial para SQLite em memória
from datetime import date

from httpx import AsyncClient, ASGITransport

# --- IMPORTS DA APLICAÇÃO ---
from app.main import app 
from app.core.database import Base
# IMPORTANTE: Importe get_db de onde seus routers importam (geralmente deps)
# Se der erro de import, mude para 'from app.core.database import get_db'
from app.core.deps import get_db 
from app.core.security import create_access_token, get_password_hash

# --- MODELS (Para as Fixtures) ---
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
    poolclass=StaticPool # Mantém os dados vivos entre conexões na mesma thread
)

TestingSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

@pytest.fixture(scope="session")
def event_loop():
    """Cria uma instância do event loop para a sessão de testes."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Cria uma sessão nova e limpa para cada teste.
    Cria as tabelas antes e dropa depois.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(db_session):
    """
    Cliente HTTP Async que sobrescreve a dependência do banco (get_db).
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()

# --- FIXTURES DE DADOS MESTRES ---

@pytest.fixture(scope="function")
async def sample_user(db_session):
    """Cria um usuário com senha hash e campos obrigatórios."""
    # Verifica existência para evitar erro de Unique Constraint
    stmt = select(User).where(User.username == "usuario_teste")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    password_hash = get_password_hash("123456")
    user = User(
        username="usuario_teste",
        email="teste@teste.com",
        nome_completo="Usuario Teste",
        password_hash=password_hash, # Campo corrigido
        ativo=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
async def usuario_normal_token(sample_user):
    """Gera um token JWT válido para o usuário de teste."""
    access_token = create_access_token(data={"sub": str(sample_user.id)})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function")
async def sample_unidade(db_session):
    """Cria uma unidade requisitante."""
    stmt = select(Unidade).where(Unidade.nome == "Unidade Teste")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    unidade = Unidade(
        codigo_administrativo="001", # Campo corrigido (era codigo)
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
    """Cria um fornecedor."""
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

# --- FIXTURES HIERÁRQUICAS (Categorias, Processos, etc) ---

@pytest.fixture(scope="function")
async def sample_categoria(db_session):
    """Cria Categoria 'Serviços' com codigo_taxonomia preenchido."""
    stmt = select(Categoria).where(Categoria.nome == "Serviços")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    cat = Categoria(
        nome="Serviços", 
        codigo_taxonomia="SV", # Campo obrigatório preenchido
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
async def sample_dfd(db_session, sample_unidade):
    """Cria um DFD pai para o processo licitatório."""
    dfd = DFD(
        numero=1,
        ano=2024,
        descricao_sucinta="DFD Teste",
        unidade_requisitante_id=sample_unidade.id, # Nome do campo corrigido (era id_unidade...)
        status="Rascunho",
        is_active=True
    )
    db_session.add(dfd)
    await db_session.commit()
    await db_session.refresh(dfd)
    return dfd

@pytest.fixture(scope="function")
async def sample_processo(db_session, sample_dfd, sample_modalidade):
    """Cria um Processo Licitatório válido vinculado ao DFD."""
    stmt = select(ProcessoLicitatorio).where(ProcessoLicitatorio.numero_processo == 1)
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    processo = ProcessoLicitatorio(
        id_dfd=sample_dfd.id,
        numero_processo=1, # Nome do campo corrigido (era numero)
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
    """
    Cria um Grupo vinculado à Categoria (Ex: 33 - Despesas Correntes).
    """
    stmt = select(Grupo).where(Grupo.codigo == "33")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    grupo = Grupo(
        categoria_id=sample_categoria.id, # FK Obrigatória
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
    """
    Cria um Subgrupo vinculado ao Grupo (Ex: 90 - Aplicações Diretas).
    """
    stmt = select(Subgrupo).where(Subgrupo.codigo == "90")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    subgrupo = Subgrupo(
        grupo_id=sample_grupo.id, # FK Obrigatória
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
    """
    Cria um Item de Catálogo válido vinculado ao Subgrupo.
    """
    # Busca usando o campo correto 'codigo_identificacao_completo'
    stmt = select(CatalogoItem).where(CatalogoItem.codigo_identificacao_completo == "1001")
    result = await db_session.execute(stmt)
    existing = result.scalars().first()
    if existing: return existing

    item = CatalogoItem(
        id_subgrupo=sample_subgrupo.id, # FK Obrigatória
        
        # Campos Obrigatórios do Model
        nome_item="Item de Catálogo Teste",
        unidade_medida="UN",
        tipo="Material",
        numero_sequencial_taxonomia="0001",
        codigo_identificacao_completo="1001", # Identificador único
        
        ativo=True
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)
    return item