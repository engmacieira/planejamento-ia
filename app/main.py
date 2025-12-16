from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings

# Core Routers
from app.routers.core import (
    auth_router,
    user_router,
    unidade_router,
    agente_router
)

# Planejamento Routers
from app.routers.planejamento import (
    dfd_router,
    etp_router,
    risk_router,
    tr_router,
    ai_router,
    cadastro_router
)

# Gestão Routers
from app.routers.gestao import (
    contrato_router,
    pedido_router,
    item_router,
    anexo_router,
    aocs_router,
    categoria_router,
    ci_pagamento_router,
    dotacao_router,
    instrumento_router,
    local_router,
    modalidade_router,
    numero_modalidade_router,
    processo_licitatorio_router,
    tipo_documento_router,
    ui_router
)
# Gestão specific Auth/User
from app.routers.gestao import auth_router as gestao_auth_router
from app.routers.gestao import user_router as gestao_user_router

app = FastAPI(
    title="Planejamento IA - ERP",
    openapi_url="/api/v1/openapi.json"
)

# Mount static files if directory exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# --- Include Routers ---

# Core
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(unidade_router.router)
app.include_router(agente_router.router)

# Planejamento
app.include_router(dfd_router.router)
app.include_router(etp_router.router)
app.include_router(risk_router.router)
app.include_router(tr_router.router)
app.include_router(ai_router.router)
app.include_router(cadastro_router.router)

# Gestão
app.include_router(contrato_router.router)
app.include_router(pedido_router.router)
app.include_router(item_router.router)
app.include_router(anexo_router.router)
app.include_router(aocs_router.router)
app.include_router(categoria_router.router)
app.include_router(ci_pagamento_router.router)
app.include_router(dotacao_router.router)
app.include_router(instrumento_router.router)
app.include_router(local_router.router)
app.include_router(modalidade_router.router)
app.include_router(numero_modalidade_router.router)
app.include_router(processo_licitatorio_router.router)
app.include_router(tipo_documento_router.router)
app.include_router(ui_router.router)
app.include_router(gestao_auth_router.router)
app.include_router(gestao_user_router.router)

@app.get("/")
def root():
    return {"message": "Bem-vindo ao Planejamento IA - ERP"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)