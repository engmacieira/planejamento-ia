from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title="Planejamento IA - ERP",
    openapi_url="/api/v1/openapi.json"
)

from app.routers import licitacao_router, gestao_router

app.include_router(licitacao_router)
app.include_router(gestao_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)