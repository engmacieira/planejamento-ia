import os
import logging
import math
import psycopg2 
from psycopg2.extras import DictCursor
from datetime import date, datetime, timezone, timedelta
from decimal import Decimal
from pydantic import BaseModel

from fastapi import (APIRouter, Depends, Form, HTTPException, Query, Request,
                     Response, status)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Body
from psycopg2.extensions import connection

from app.core.security import (ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token,
                               get_current_user, require_access_level)
from app.models.core.user_model import User
from app.repositories.core.user_repository import UserRepository 

from types import SimpleNamespace

from app.core.database import get_db
# Repositories (Gestão)
from app.repositories.gestao.categoria_repository import CategoriaRepository
from app.repositories.gestao.contrato_repository import ContratoRepository
from app.repositories.gestao.item_repository import ItemRepository
from app.repositories.gestao.aocs_repository import AocsRepository
from app.repositories.gestao.pedido_repository import PedidoRepository
from app.repositories.gestao.ci_pagamento_repository import CiPagamentoRepository
from app.repositories.gestao.anexo_repository import AnexoRepository
from app.repositories.core.unidade_repository import UnidadeRepository
from app.repositories.gestao.local_repository import LocalRepository
from app.repositories.core.agente_repository import AgenteRepository
from app.repositories.gestao.dotacao_repository import DotacaoRepository
from app.repositories.gestao.tipo_documento_repository import TipoDocumentoRepository
from app.repositories.gestao.instrumento_repository import InstrumentoRepository
from app.repositories.gestao.modalidade_repository import ModalidadeRepository
from app.repositories.gestao.numero_modalidade_repository import NumeroModalidadeRepository
from app.repositories.gestao.processo_licitatorio_repository import ProcessoLicitatorioRepository
from app.schemas.gestao.ci_pagamento_schema import CiPagamentoCreateRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["Gestão - UI"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ajuste: O arquivo agora está em app/routers/gestao/ui_router.py.
# Templates estão em .../app/templates? Ou .../templates?
# Supondo estrutura:
# root/
#   app/
#     routers/
#       gestao/
#         ui_router.py
#     templates/
#
# BASE_DIR será .../app/routers/gestao
# Precisamos subir 2 niveis para chegar em app/ e depois entrar em templates
# Ou se estiver em root/templates: subir 3 niveis.
# Vamos assumir que 'templates' está em 'app/templates' ou 'sistemas/gestao/templates' (legacy)
# O código original era: TEMPLATES_DIR = os.path.join(os.path.dirname(BASE_DIR), "templates")
# Se BASE_DIR era app/routers (em sistemas/gestao/app/routers), subir um nivel dava sistemas/gestao/app. E lá tinha templates?
# Vamos tentar manter flexível ou procurar onde estão os templates.
# Assumirei que templates estarão em app/templates no novo projeto unificado.
# BASE_DIR = .../app/routers/gestao
# dirname(BASE_DIR) = .../app/routers
# dirname(...) = .../app
# join(..., "templates") = .../app/templates

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "templates")
# Se não existir, tenta o caminho legado (só para garantir em dev)
if not os.path.exists(TEMPLATES_DIR):
     # Tenta .../sistemas/gestao/templates
     # Mas estamos movendo arquivos. O ideal é que o usuario tenha movido templates tambem.
     # Vamos manter app/templates.
     pass

templates = Jinja2Templates(directory=TEMPLATES_DIR)

try:
    from num2words import num2words
    templates.env.globals['num2words'] = num2words
except ImportError:
    logger.warning("Biblioteca 'num2words' não encontrada. A função por extenso não funcionará.")
    templates.env.globals['num2words'] = lambda x, **kwargs: f"Erro: num2words não instalada ({x})"


VERSAO_SOFTWARE = "3.0.0" 
ITENS_POR_PAGINA = 10 

templates.env.globals['versao_software'] = VERSAO_SOFTWARE

class ItemGenerico(BaseModel):
    nome: str
    
TABELAS_GERENCIAVEIS = {
    'instrumento-contratual': {
        'repo': InstrumentoRepository, 
        'titulo': 'Instrumentos Contratuais',
        'coluna': 'nome' 
    },
    'modalidade': {
        'repo': ModalidadeRepository, 
        'titulo': 'Modalidades',
        'coluna': 'nome'
    },
    'numero-modalidade': {
        'repo': NumeroModalidadeRepository, 
        'titulo': 'Números de Modalidade',
        'coluna': 'numero_ano' 
    },
    'processo-licitatorio': {
        'repo': ProcessoLicitatorioRepository, 
        'titulo': 'Processos Licitatórios',
        'coluna': 'numero' 
    },
    'unidade-requisitante': {
        'repo': UnidadeRepository, 
        'titulo': 'Unidades Requisitantes',
        'coluna': 'nome'
    },
    'local-entrega': {
        'repo': LocalRepository, 
        'titulo': 'Locais de Entrega',
        'coluna': 'descricao' 
    },
    'agente-responsavel': {
        'repo': AgenteRepository, 
        'titulo': 'Agentes Responsáveis',
        'coluna': 'nome'
    },
    'dotacao': {
        'repo': DotacaoRepository, 
        'titulo': 'Dotações Orçamentárias',
        'coluna': 'info_orcamentaria' 
    },
    'tipo-documento': {
        'repo': TipoDocumentoRepository, 
        'titulo': 'Tipos de Documento',
        'coluna': 'nome'
    }
}
ENTIDADES_PESQUISAVEIS = { 
    'processo_licitatorio': {'label': 'Contratos por Processo Licitatório', 'tabela_principal': 'processoslicitatorios', 'coluna_texto': 'numero'},
    'unidade_requisitante': {'label': 'AOCS por Unidade Requisitante', 'tabela_principal': 'unidadesrequisitantes', 'coluna_texto': 'nome'},
    'local_entrega': {'label': 'AOCS por Local de Entrega', 'tabela_principal': 'locaisentrega', 'coluna_texto': 'descricao'},
    'dotacao': {'label': 'AOCS por Dotação Orçamentária', 'tabela_principal': 'dotacao', 'coluna_texto': 'info_orcamentaria'}
}
RELATORIOS_DISPONIVEIS = { 
    'lista_fornecedores': {'titulo': 'Lista de Fornecedores', 'descricao': '...', 'ordenacao_opcoes': {}},
    'lista_contratos': {'titulo': 'Lista de Contratos Ativos', 'descricao': '...', 'ordenacao_opcoes': {}}
}

@router.get("/login", response_class=HTMLResponse, name="login")
async def login_ui(request: Request, msg: str = None, category: str = None):
    """Renderiza a página de login."""
    context = {
        "messages": [(category, msg)] if msg and category else None,
        "get_flashed_messages": lambda **kwargs: [(category, msg)] if msg and category else []
    }
    return templates.TemplateResponse(request, "login.html", context)

@router.post("/login", name="login_post")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db_conn: connection = Depends(get_db) 
):
    """Processa o formulário de login, autentica e define o cookie."""
    user_repo = UserRepository(db_conn)
    user = user_repo.get_by_username(username)

    if not user or not user.verificar_senha(password):
        login_url = request.app.url_path_for("login")
        return RedirectResponse(
            url=f"{login_url}?msg=Usuário ou senha inválidos.&category=error",
            status_code=status.HTTP_302_FOUND
        )

    access_token = create_access_token(user=user)
    token_type = "bearer"

    response = RedirectResponse(url=request.app.url_path_for("home_ui"), status_code=status.HTTP_302_FOUND)
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires = datetime.now(timezone.utc) + expires_delta

    response.set_cookie(
        key="access_token",
        value=f"{token_type} {access_token}",
        expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"), 
        httponly=True,
        samesite="lax",
        secure=False, 
        path="/"
    )
    return response

@router.get("/logout", name="logout")
async def logout(request: Request): 
    response = RedirectResponse(
        url=f"{request.app.url_path_for('login')}?msg=Você foi desconectado com sucesso.&category=success",
        status_code=status.HTTP_302_FOUND
    )
    response.delete_cookie(key="access_token", path="/", httponly=True)
    return response

@router.get("/", response_class=RedirectResponse, include_in_schema=False)
async def read_root(request: Request):
    return RedirectResponse(url=request.app.url_path_for("login"))

@router.get("/home", response_class=HTMLResponse, name="home_ui", dependencies=[Depends(require_access_level(3))])
async def home_ui(
    request: Request, 
    page: int = Query(1, alias="page"), # Recebe o número da página
    current_user=Depends(get_current_user), 
    db_conn: connection = Depends(get_db)
):
    indicadores = {"contratos_ativos": 0, "pedidos_mes": 0, "contratos_a_vencer": 0}
    
    # Variáveis de Paginação
    pedidos_pendentes = []
    total_paginas = 1
    ITENS_DASHBOARD = 10 # Limite por página
    
    try:
         # 1. Indicadores (Lógica existente mantida)
         cursor = db_conn.cursor()
         cursor.execute("SELECT COUNT(id) FROM Contratos WHERE ativo = TRUE")
         indicadores["contratos_ativos"] = cursor.fetchone()[0]
         cursor.close()
         
         # 2. Pedidos Pendentes Paginados (NOVA LÓGICA)
         pedido_repo = PedidoRepository(db_conn)
         resultado = pedido_repo.get_pendentes_paginados(page=page, limit=ITENS_DASHBOARD)
         
         pedidos_pendentes = resultado['itens']
         total_registros = resultado['total']
         
         # Cálculo de páginas (Arredonda para cima: 11 itens / 10 = 1.1 -> 2 páginas)
         if total_registros > 0:
             total_paginas = math.ceil(total_registros / ITENS_DASHBOARD)
         
    except Exception as e:
         logger.error(f"Erro ao buscar dados do dashboard: {e}")

    # Passamos os query_params para o macro de paginação não perder filtros (se houver no futuro)
    query_params = dict(request.query_params)

    context = {
        "current_user": current_user,
        "indicadores": indicadores,
        "pedidos_pendentes": pedidos_pendentes,
        
        # Variáveis necessárias para o _pagination.html funcionar
        "pagina_atual": page,
        "total_paginas": total_paginas,
        "query_params": query_params,
        
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "index.html", context)

@router.get("/categorias-ui", response_class=HTMLResponse, name="categorias_ui", dependencies=[Depends(require_access_level(3))])
async def categorias_ui(
    request: Request,
    page: int = Query(1, alias="page"),
    mostrar_inativos: bool = Query(False),
    sort_by: str = Query('id'),
    order: str = Query('asc'),
    current_user=Depends(get_current_user),
    db_conn: connection = Depends(get_db)
):
    repo = CategoriaRepository(db_conn)
    categorias_db = []
    total_paginas = 1
    try:
        categorias_db = repo.get_all(mostrar_inativos=mostrar_inativos)
        offset = (page - 1) * ITENS_POR_PAGINA
        total_itens = len(categorias_db)
        categorias_paginadas = categorias_db[offset:offset + ITENS_POR_PAGINA]
        total_paginas = math.ceil(total_itens / ITENS_POR_PAGINA)

    except Exception as e:
        logger.error(f"Erro ao buscar categorias para UI: {e}")

    query_params = dict(request.query_params)

    context = {
        "current_user": current_user,
        "categorias": categorias_paginadas, 
        "pagina_atual": page,
        "total_paginas": total_paginas,
        "query_params": query_params,
        "mostrar_inativos": mostrar_inativos,
        "sort_by": sort_by,
        "order": order,
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "categorias.html", context)

@router.get("/contratos-ui", response_class=HTMLResponse, name="contratos_ui", dependencies=[Depends(require_access_level(3))])
async def contratos_ui(
    request: Request,
    page: int = Query(1, alias="page"),
    busca: str | None = Query(None),
    status: str | None = Query(None),
    sort_by: str = Query('numero_contrato'),
    order: str = Query('asc'),
    mostrar_vencidos: str | None = Query(None),
    data_vencimento_filtro: str | None = Query(None),
    current_user=Depends(get_current_user),
    db_conn: connection = Depends(get_db)
):
    contratos_view = [] 
    total_paginas = 1
    hoje = date.today()

    try:
        logger.info(f"Buscando contratos: page={page}, busca={busca}, status={status}, sort={sort_by}, order={order}, mv={mostrar_vencidos}, dvf={data_vencimento_filtro}")

        repo = ContratoRepository(db_conn)
        todos_contratos = repo.get_all(mostrar_inativos=True)

        contratos_filtrados = todos_contratos

        if busca:
            termo = busca.lower()
            contratos_filtrados = [
                c for c in contratos_filtrados
                if termo in c.numero_contrato.lower() or (c.fornecedor and termo in c.fornecedor.nome.lower())
            ]

        if status == 'ativo':
            contratos_filtrados = [c for c in contratos_filtrados if c.ativo and c.data_fim >= hoje]
        elif status == 'inativo':
            contratos_filtrados = [c for c in contratos_filtrados if not c.ativo or (c.ativo and c.data_fim < hoje)]
        elif status == 'expirado':
             contratos_filtrados = [c for c in contratos_filtrados if c.data_fim < hoje]

        if mostrar_vencidos == 'false':
             contratos_filtrados = [c for c in contratos_filtrados if c.data_fim >= hoje]

        if data_vencimento_filtro == '60d':
             limite_vencimento = hoje + timedelta(days=60)
             contratos_filtrados = [c for c in contratos_filtrados if c.ativo and c.data_fim >= hoje and c.data_fim <= limite_vencimento]

        reverse_order = (order == 'desc')
        if sort_by == 'numero_contrato':
             contratos_filtrados.sort(key=lambda c: c.numero_contrato, reverse=reverse_order)
        elif sort_by == 'fornecedor':
             contratos_filtrados.sort(key=lambda c: c.fornecedor.nome if c.fornecedor else "", reverse=reverse_order)
        elif sort_by == 'data_vigencia_fim':
             contratos_filtrados.sort(key=lambda c: c.data_fim, reverse=reverse_order)
        elif sort_by == 'status_ativo':
             contratos_filtrados.sort(key=lambda c: c.ativo, reverse=reverse_order)
        offset = (page - 1) * ITENS_POR_PAGINA
        total_itens = len(contratos_filtrados)
        contratos_paginados = contratos_filtrados[offset:offset + ITENS_POR_PAGINA]
        total_paginas = math.ceil(total_itens / ITENS_POR_PAGINA) if total_itens > 0 else 1

        cat_repo = CategoriaRepository(db_conn)
        proc_repo = ProcessoLicitatorioRepository(db_conn)
        for c in contratos_paginados:
             proc = proc_repo.get_by_id(c.id_processo_licitatorio) 
             
             dt_fim_normalizada = c.data_fim
             if isinstance(dt_fim_normalizada, datetime):
                 dt_fim_normalizada = dt_fim_normalizada.date()
             elif isinstance(dt_fim_normalizada, str):
                 try:
                     dt_fim_normalizada = datetime.strptime(dt_fim_normalizada, '%Y-%m-%d').date()
                 except:
                     dt_fim_normalizada = None
                     
             contratos_view.append({
                 'id': c.id,
                 'numero_contrato': c.numero_contrato,
                 'processo_licitatorio': proc.numero if proc else 'N/D',
                 'fornecedor': c.fornecedor.nome if c.fornecedor else 'N/D',
                 'data_vigencia_fim': c.data_fim,
                 'status_ativo': c.ativo,
             })

    except Exception as e:
        logger.exception(f"Erro ao buscar contratos para UI: {e}")

    query_params = dict(request.query_params)

    context = {
        "request": request,
        "current_user": current_user,
        "contratos": contratos_view,
        "pagina_atual": page,
        "total_paginas": total_paginas,
        "query_params": query_params,
        "sort_by": sort_by,
        "order": order,
        "hoje": hoje,
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "contratos.html", context)
    
@router.get("/pedidos-ui", response_class=HTMLResponse, name="pedidos_ui", dependencies=[Depends(require_access_level(3))])
async def pedidos_ui(
    request: Request, 
    page: int = Query(1, alias="page"),
    busca: str | None = Query(None),
    sort_by: str = Query('data'), 
    order: str = Query('desc'),
    current_user=Depends(get_current_user), 
    db_conn: connection = Depends(get_db)
):
    aocs_repo = AocsRepository(db_conn) 
    pedido_repo = PedidoRepository(db_conn)
    item_repo = ItemRepository(db_conn)
    contrato_repo = ContratoRepository(db_conn)
    
    todas_aocs = aocs_repo.get_all()
    
    aocs_view = []
    
    for aocs in todas_aocs:
        itens_pedidos = pedido_repo.get_by_aocs_id(aocs.id)
        
        valor_total_aocs = Decimal('0.0')
        nome_fornecedor = "N/D"
        status_consolidado = "Pendente"
        
        total_qtd_pedida = Decimal('0.0')
        total_qtd_entregue = Decimal('0.0')

        for p in itens_pedidos:
            item = item_repo.get_by_id(p.id_item_contrato)
            if item:
                subtotal = p.quantidade_pedida * item.valor_unitario
                valor_total_aocs += subtotal
                
                total_qtd_pedida += p.quantidade_pedida
                total_qtd_entregue += p.quantidade_entregue

                if nome_fornecedor == "N/D":
                    contrato = contrato_repo.get_by_id(item.id_contrato)
                    if contrato and contrato.fornecedor:
                        nome_fornecedor = contrato.fornecedor.nome

        if total_qtd_pedida > 0:
            if total_qtd_entregue >= total_qtd_pedida:
                status_consolidado = "Entregue"
            elif total_qtd_entregue > 0:
                status_consolidado = "Parcial"
            else:
                status_consolidado = "Pendente"
        elif not itens_pedidos:
             status_consolidado = "Vazio" 

        if busca:
            termo = busca.lower()
            match_aocs = (termo in aocs.numero_aocs.lower())
            match_forn = (termo in nome_fornecedor.lower())
            
            if not (match_aocs or match_forn):
                continue
        
        aocs_view.append({
            "id": aocs.id,
            "numero_aocs": aocs.numero_aocs,
            "numero_pedido": aocs.numero_pedido, 
            "fornecedor": nome_fornecedor,
            "valor_total": valor_total_aocs,
            "status_entrega": status_consolidado,
            "data_pedido": aocs.data_criacao
        })

    reverse_order = (order == 'desc')
    
    def get_sort_key(item, key_name, default_val=''):
        val = item.get(key_name)
        if val is None: val = default_val
        return (val, item['id'])

    if sort_by == 'aocs':
        aocs_view.sort(key=lambda x: get_sort_key(x, 'numero_aocs'), reverse=reverse_order)
    elif sort_by == 'fornecedor':
        aocs_view.sort(key=lambda x: get_sort_key(x, 'fornecedor'), reverse=reverse_order)
    elif sort_by == 'valor':
        aocs_view.sort(key=lambda x: (x['valor_total'], x['id']), reverse=reverse_order)
    elif sort_by == 'status':
        aocs_view.sort(key=lambda x: get_sort_key(x, 'status_entrega'), reverse=reverse_order)
    else: 
        aocs_view.sort(key=lambda x: (x['data_pedido'] if x['data_pedido'] else date.min, x['id']), reverse=reverse_order)

    total_itens = len(aocs_view)
    offset = (page - 1) * ITENS_POR_PAGINA
    pedidos_paginados = aocs_view[offset:offset + ITENS_POR_PAGINA]
    total_paginas = math.ceil(total_itens / ITENS_POR_PAGINA) if total_itens > 0 else 1

    query_params = dict(request.query_params)

    context = {
        "request": request,
        "current_user": current_user,
        "pedidos_lista": pedidos_paginados, 
        "pagina_atual": page, 
        "total_paginas": total_paginas,
        "query_params": query_params, 
        "sort_by": sort_by, 
        "order": order, 
        "termo_busca": busca,
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "pedidos.html", context)

@router.get("/consultas", response_class=HTMLResponse, name="consultas_ui", dependencies=[Depends(require_access_level(3))])
async def consultas_ui(request: Request, current_user=Depends(get_current_user)):
    context = {
        "current_user": current_user,
        "entidades_pesquisaveis": ENTIDADES_PESQUISAVEIS, 
        "processos": [], "unidades": [], "locais": [], "dotacoes": [],
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "consultas.html", context)

@router.get("/relatorios", response_class=HTMLResponse, name="relatorios_ui", dependencies=[Depends(require_access_level(3))])
async def relatorios_ui(request: Request, current_user=Depends(get_current_user)):
    context = {
        "current_user": current_user,
        "relatorios": RELATORIOS_DISPONIVEIS, 
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "relatorios.html", context)

@router.get("/importar", response_class=HTMLResponse, name="importar_ui", dependencies=[Depends(require_access_level(2))])
async def importar_ui(request: Request, current_user=Depends(get_current_user)):
    context = {"current_user": current_user, "get_flashed_messages": lambda **kwargs: []}
    return templates.TemplateResponse(request, "importar.html", context)

@router.get("/contratos/novo", response_class=HTMLResponse, name="novo_contrato_ui", dependencies=[Depends(require_access_level(2))])
async def novo_contrato_ui(
    request: Request, 
    current_user=Depends(get_current_user),
    db_conn: connection = Depends(get_db)
):
    cat_repo = CategoriaRepository(db_conn)
    inst_repo = InstrumentoRepository(db_conn)
    mod_repo = ModalidadeRepository(db_conn)
    num_mod_repo = NumeroModalidadeRepository(db_conn)
    proc_repo = ProcessoLicitatorioRepository(db_conn)

    context = {
        "request": request,
        "current_user": current_user,
        "categorias": cat_repo.get_all(),
        "instrumentos": inst_repo.get_all(),
        "modalidades": mod_repo.get_all(),
        "numeros_modalidade": num_mod_repo.get_all(),
        "processos": proc_repo.get_all(),
        "get_flashed_messages": lambda **kwargs: []
    }
    
    return templates.TemplateResponse(request, "novo_contrato.html", context)

@router.get("/gerenciar-tabelas", response_class=HTMLResponse, name="gerenciar_tabelas_ui", dependencies=[Depends(require_access_level(2))])
async def gerenciar_tabelas_ui(request: Request, current_user=Depends(get_current_user)):
    context = {
        "current_user": current_user,
        "tabelas": TABELAS_GERENCIAVEIS,
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "gerenciar_tabelas.html", context)

@router.get("/admin/usuarios", response_class=HTMLResponse, name="gerenciar_usuarios_ui", dependencies=[Depends(require_access_level(1))])
async def gerenciar_usuarios_ui(request: Request, current_user=Depends(get_current_user), db_conn: connection = Depends(get_db)):
    repo = UserRepository(db_conn)
    usuarios = []
    try:
        usuarios = repo.get_all(mostrar_inativos=True)
    except Exception as e:
        logger.error(f"Erro ao buscar usuários para UI admin: {e}")

    context = {
        "current_user": current_user,
        "usuarios": usuarios,
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "gerenciar_usuarios.html", context)

@router.get("/contrato/{id_contrato}", response_class=HTMLResponse, name="detalhe_contrato", dependencies=[Depends(require_access_level(3))])
async def detalhe_contrato(request: Request, id_contrato: int, current_user=Depends(get_current_user), db_conn: connection = Depends(get_db)):
    contrato_repo = ContratoRepository(db_conn)
    item_repo = ItemRepository(db_conn)
    anexo_repo = AnexoRepository(db_conn)
    tipo_doc_repo = TipoDocumentoRepository(db_conn)

    contrato = contrato_repo.get_by_id(id_contrato)
    if not contrato: raise HTTPException(status_code=404, detail="Contrato não encontrado")

    itens = item_repo.get_by_contrato_id(id_contrato)
    anexos = anexo_repo.get_by_entidade(id_entidade=id_contrato, tipo_entidade='contrato')
    tipos_documento = [td.nome for td in tipo_doc_repo.get_all()] 

    cat_repo = CategoriaRepository(db_conn)
    inst_repo = InstrumentoRepository(db_conn)
    mod_repo = ModalidadeRepository(db_conn)
    num_mod_repo = NumeroModalidadeRepository(db_conn)
    proc_repo = ProcessoLicitatorioRepository(db_conn)

    categoria = cat_repo.get_by_id(contrato.id_categoria)
    instrumento = inst_repo.get_by_id(contrato.id_instrumento_contratual)
    modalidade = mod_repo.get_by_id(contrato.id_modalidade)
    num_modalidade = num_mod_repo.get_by_id(contrato.id_numero_modalidade)
    processo = proc_repo.get_by_id(contrato.id_processo_licitatorio)

    contrato_view = {
        "id": contrato.id,
        "numero_contrato": contrato.numero_contrato,
        "fornecedor": contrato.fornecedor.nome,
        "cpf_cnpj": contrato.fornecedor.cpf_cnpj,
        "email": contrato.fornecedor.email,
        "telefone": contrato.fornecedor.telefone,
        "data_inicio_br": contrato.data_inicio.strftime('%d/%m/%Y'),
        "data_fim_br": contrato.data_fim.strftime('%d/%m/%Y'),
        "nome_categoria": categoria.nome if categoria else 'N/D',
        "nome_instrumento": instrumento.nome if instrumento else 'N/D',
        "nome_modalidade": modalidade.nome if modalidade else 'N/D',
        "numero_modalidade_ano": num_modalidade.numero_ano if num_modalidade else 'N/D',
        "numero_processo": processo.numero if processo else 'N/D',
    }


    context = {
        "current_user": current_user,
        "contrato": contrato_view, "itens": itens, "anexos": anexos,
        "tipos_documento": tipos_documento,
        "pagina_atual": 1, "total_paginas": 1, 
        "query_params": dict(request.query_params), "sort_by": 'numero_item', "order": 'asc', 
        "get_flashed_messages": lambda **kwargs: []
    }
    
    return templates.TemplateResponse(request, "detalhe_contrato.html", context)

@router.get("/contrato/{id_contrato}/importar-itens", response_class=HTMLResponse, name="importar_itens_ui", dependencies=[Depends(require_access_level(2))])
async def importar_itens_ui(
    request: Request, 
    id_contrato: int, 
    current_user=Depends(get_current_user), 
    db_conn: connection = Depends(get_db)
):
    contrato_repo = ContratoRepository(db_conn)
    contrato = contrato_repo.get_by_id(id_contrato)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")

    contrato_view = {
        "id": contrato.id,
        "numero_contrato": contrato.numero_contrato,
    }

    context = {
        "url_for": request.app.url_path_for, 
        "current_user": current_user,
        "contrato": contrato_view,
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "importar_itens.html", context)

@router.get("/categoria/{id_categoria}/contratos", response_class=HTMLResponse, name="contratos_por_categoria", dependencies=[Depends(require_access_level(3))])
async def contratos_por_categoria(
    request: Request, 
    id_categoria: int, 
    page: int = Query(1, alias="page"),
    busca: str = Query(None),
    sort_by: str = Query("descricao"),
    order: str = Query("asc"),
    current_user=Depends(get_current_user), 
    db_conn: connection = Depends(get_db)
):
    cat_repo = CategoriaRepository(db_conn)
    categoria = cat_repo.get_by_id(id_categoria)
    if not categoria: 
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    itens = []
    total_paginas = 1
    query_params = dict(request.query_params)

    ITENS_POR_PAGINA = 10 
    cursor = None

    try:
        cursor = db_conn.cursor(cursor_factory=DictCursor)

        params = [id_categoria]
        where_clause = "WHERE c.id_categoria = %s AND c.ativo = TRUE AND ic.ativo = TRUE"

        if busca:
            where_clause += " AND ic.descricao ILIKE %s"
            params.append(f"%{busca}%")

        colunas_ordenaveis = {
            'descricao': 'ic.descricao', 
            'contrato': 'c.numero_contrato',
            'saldo': 'saldo', 
            'valor': 'ic.valor_unitario', 
            'numero_item': 'ic.numero_item'
        }
        coluna_ordenacao = colunas_ordenaveis.get(sort_by, 'ic.descricao')
        direcao_ordenacao = 'DESC' if order == 'desc' else 'ASC'
        order_by_clause = f"ORDER BY {coluna_ordenacao} {direcao_ordenacao}"

        offset = (page - 1) * ITENS_POR_PAGINA
        limit_offset_clause = "LIMIT %s OFFSET %s"
        params.extend([ITENS_POR_PAGINA, offset])

        sql_select = f"""
            SELECT
                ic.*, 
                c.id AS id_contrato, 
                c.numero_contrato, 
                c.fornecedor,
                COALESCE(pedidos_sum.total_pedido, 0) AS total_pedido,
                (ic.quantidade - COALESCE(pedidos_sum.total_pedido, 0)) AS saldo,
                COUNT(*) OVER() as total_geral
            FROM itenscontrato ic
            JOIN contratos c ON ic.id_contrato = c.id
            LEFT JOIN (
                SELECT id_item_contrato, SUM(quantidade_pedida) as total_pedido
                FROM pedidos GROUP BY id_item_contrato
            ) AS pedidos_sum ON ic.id = pedidos_sum.id_item_contrato
            {where_clause} 
            {order_by_clause} 
            {limit_offset_clause}
        """

        cursor.execute(sql_select, params)
        itens_db = cursor.fetchall()

        total_itens = 0
        if itens_db:
            total_itens = itens_db[0]['total_geral']
        total_paginas = math.ceil(total_itens / ITENS_POR_PAGINA)

        itens = [dict(item) for item in itens_db]

    except (Exception, psycopg2.DatabaseError) as error:
         if cursor: cursor.close()
         logger.exception(f"Erro ao buscar itens com saldo para UI Categoria ID {id_categoria}: {error}")
         query_params["erro"] = "Erro ao consultar o banco de dados."
    finally:
        if cursor: cursor.close()

    context = {
        "current_user": current_user,
        "categoria": categoria, 
        "itens": itens, 
        "pagina_atual": page, 
        "total_paginas": total_paginas,
        "query_params": query_params, 
        "sort_by": sort_by, 
        "order": order,
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "contratos_por_categoria.html", context)


@router.get("/categoria/{id_categoria}/novo-pedido", response_class=HTMLResponse, name="novo_pedido_pagina", dependencies=[Depends(require_access_level(2))])
async def novo_pedido_pagina(request: Request, id_categoria: int, current_user=Depends(get_current_user), db_conn: connection = Depends(get_db)):
    cat_repo = CategoriaRepository(db_conn)
    categoria = cat_repo.get_by_id(id_categoria)
    if not categoria: raise HTTPException(status_code=404, detail="Categoria não encontrada")

    unidade_repo = UnidadeRepository(db_conn)
    local_repo = LocalRepository(db_conn)
    agente_repo = AgenteRepository(db_conn)
    dotacao_repo = DotacaoRepository(db_conn)

    context = {
        "current_user": current_user,
        "categoria": categoria,
        "unidades": [u.nome for u in unidade_repo.get_all()],
        "locais": [l.descricao for l in local_repo.get_all()],
        "responsaveis": [a.nome for a in agente_repo.get_all()],
        "dotacoes": [d.info_orcamentaria for d in dotacao_repo.get_all()],
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "novo_pedido.html", context)

@router.get("/pedido/{numero_aocs:path}/nova-ci", response_class=HTMLResponse, name="nova_ci_ui", dependencies=[Depends(require_access_level(2))])
async def nova_ci_ui(
    request: Request, 
    numero_aocs: str, 
    current_user=Depends(get_current_user), 
    db_conn: connection = Depends(get_db)
):
    aocs_repo = AocsRepository(db_conn)
    dotacao_repo = DotacaoRepository(db_conn)
    agente_repo = AgenteRepository(db_conn)
    unidade_repo = UnidadeRepository(db_conn)
    
    aocs = aocs_repo.get_by_numero_aocs(numero_aocs)
    if not aocs:
        raise HTTPException(status_code=404, detail="AOCS não encontrada.")

    primeiro_fornecedor = 'N/D'
    primeiro_cnpj = 'N/D'
    pedido_repo = PedidoRepository(db_conn)
    item_repo = ItemRepository(db_conn)
    contrato_repo = ContratoRepository(db_conn)
    
    pedidos = pedido_repo.get_by_aocs_id(aocs.id)
    if pedidos:
        item = item_repo.get_by_id(pedidos[0].id_item_contrato)
        contrato = contrato_repo.get_by_id(item.id_contrato) if item else None
        if contrato and contrato.fornecedor:
            primeiro_fornecedor = contrato.fornecedor.nome
            primeiro_cnpj = contrato.fornecedor.cpf_cnpj
            
    aocs_view = {
        "id": aocs.id,
        "justificativa": aocs.justificativa,
        "fornecedor": primeiro_fornecedor,
        "cpf_cnpj": primeiro_cnpj,
        "id_unidade_requisitante": aocs.id_unidade_requisitante,
        "id_agente_responsavel": aocs.id_agente_responsavel,
        "id_dotacao": aocs.id_dotacao
    }

    dotacoes = dotacao_repo.get_all()
    solicitantes = agente_repo.get_all()
    secretarias = unidade_repo.get_all()

    context = {
        "current_user": current_user,
        "aocs": aocs_view,
        "dotacoes": [d.info_orcamentaria for d in dotacoes],
        "solicitantes": [a.nome for a in solicitantes],
        "secretarias": [u.nome for u in secretarias],
        "get_flashed_messages": lambda **kwargs: []
    }
    return templates.TemplateResponse(request, "nova_ci.html", context)
