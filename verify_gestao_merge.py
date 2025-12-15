import os
# Mocking env vars for testing imports if they are missing
os.environ["SECRET_KEY"] = "test_secret"
os.environ["DB_URL"] = "postgresql://user:pass@localhost/db"

try:
    from app.core.config import settings
    from app.core.security import get_password_hash, verify_password, create_access_token
    from app.core.logging_config import setup_logging
    
    print("✅ Imports successful.")
    
    # Test Hashing
    pwd = "teste"
    hashed = get_password_hash(pwd)
    print(f"✅ Hash generated: {hashed}")
    
    if verify_password(pwd, hashed):
        print("✅ Password verified.")
    else:
        print("❌ Password verification failed.")

    # Test Logging Setup
    setup_logging()
    print("✅ Logging setup called.")

except Exception as e:
    print(f"❌ Error during verification: {e}")
    exit(1)
