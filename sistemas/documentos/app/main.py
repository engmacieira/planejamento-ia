from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importações do Core e Banco de Dados
from app.core.database import engine, Base

# Importações dos Roteadores
from app.routers import user_router, auth_router, process_router
# from app.routers import template_router # (Opcional: mantido comentado caso queira usar no futuro)

# 1. CRIAÇÃO DAS TABELAS
# Isso garante que o arquivo app.db seja criado com as tabelas (users, processos, logs)
# assim que o sistema iniciar.
Base.metadata.create_all(bind=engine)

# 2. INICIALIZAÇÃO DO APP
app = FastAPI(title="Fábrica de Processos")

# 3. CONFIGURAÇÃO DO CORS
# Permite que o Frontend (mesmo rodando em outra porta) converse com o Backend.
# Em produção, você trocaria "*" pela lista de domínios permitidos.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. MONTAGEM DOS ARQUIVOS ESTÁTICOS (FRONTEND)
# Isso faz com que tudo que estiver na pasta 'static' seja acessível pelo navegador.
# Ex: http://localhost:8000/static/index.html
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# 5. REGISTRO DAS ROTAS (ENDPOINTS)
app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(process_router.router)
# app.include_router(template_router.router)

# 6. ROTA RAIZ (Health Check)
@app.get("/")
def read_root():
    return {
        "message": "Fábrica de Processos Online!",
        "docs": "Acesse /docs para ver a documentação da API",
        "frontend": "Acesse /static/ para usar o sistema"
    }