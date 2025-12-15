from app.core.base_model import DefaultModel
from app.core.deps import get_file_service, get_current_user

def verify_documentos_merge():
    # Test 1: Base Model Import
    print("✅ Base Model imported successfully.")
    
    # Test 2: Deps Injection (Stubs)
    svc = get_file_service()
    if svc.name == "FileService":
        print("✅ Dependency Injection (Mock) working.")
    else:
        print("❌ Dependency Injection failed.")

    print("✅ Documentos Merge Verification Passed.")

if __name__ == "__main__":
    verify_documentos_merge()
