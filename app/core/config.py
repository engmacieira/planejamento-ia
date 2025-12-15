from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Metadata
    PROJECT_NAME: str = "LicitaFlow API"
    API_V1_STR: str = "/api/v1"

    # Definimos aqui EXATAMENTE o que tem no seu .env
    DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email Settings (Legacy compatibility & Future use)
    EMAIL_HOST: str | None = None
    EMAIL_PORT: int | None = 587
    EMAIL_USER: str | None = None
    EMAIL_PASSWORD: str | None = None
    EMAIL_FROM: str | None = None
    
    # Opcional (None) caso você ainda não tenha colocado, para não quebrar
    GEMINI_API_KEY: str | None = None 
    
    # Se o código antigo tinha variaveis separadas (POSTGRES_USER), 
    # nós removemos daqui porque vamos usar a URL completa.

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # Isso aqui é o pulo do gato: se tiver coisa extra no .env, ele ignora em vez de dar erro
        extra="ignore" 
    )

settings = Settings()