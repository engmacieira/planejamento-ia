from app.core.config import settings

def verify_config():
    print("Verifying Settings:")
    print(f"PROJECT_NAME: {settings.PROJECT_NAME}")
    print(f"API_V1_STR: {settings.API_V1_STR}")
    print(f"DB_URL: {settings.DB_URL}")
    print(f"GEMINI_API_KEY: {'[SET]' if settings.GEMINI_API_KEY else '[NOT SET]'}")
    
    if not settings.DB_URL:
        print("❌ DB_URL not found!")
    else:
        print("✅ Config loaded successfully.")

if __name__ == "__main__":
    verify_config()
