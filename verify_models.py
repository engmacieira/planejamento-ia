import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from app.models.gestao.contrato import Contrato
    from app.models.gestao.item import Item
    from app.models.gestao.fornecedor import Fornecedor
    
    print("Successfully imported models.")
    print(f"Contrato table: {Contrato.__tablename__}")
    print(f"Item table: {Item.__tablename__}")
    print(f"Fornecedor table: {Fornecedor.__tablename__}")

except Exception as e:
    print(f"Error validating models: {e}")
    sys.exit(1)
