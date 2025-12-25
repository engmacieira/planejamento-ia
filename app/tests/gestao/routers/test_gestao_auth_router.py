import pytest
import io
from app.models.core.anexo_model import Anexo

@pytest.mark.asyncio
async def test_upload_anexo_success(client, usuario_normal_token, db_session):
    # Mock file upload
    file_content = b"fake pdf content"
    files = {
        'file': ("teste.pdf", file_content, "application/pdf")
    }
    data = {
        "tipo_entidade": "contrato",
        "id_entidade": "1",
        "tipo_documento": "Contrato",
        "tipo_documento_novo": ""
    }
    
    # Needs auth
    r = await client.post("/anexos/upload/", files=files, data=data, headers=usuario_normal_token)
    
    # If folder creation fails or permission issues in test env, might error 500.
    # But usually temp dir is writable.
    # Also, dependencies like 'get_db' are overridden by client fixture? 
    # Yes, client fixture uses 'override_get_db' (from conftest).
    # But Router uses 'db_conn: connection = Depends(get_db)' - type hint says connection (psycopg2) but local tests use AsyncSession or equivalent?
    # Our conftest uses AsyncSession. The code might be expecting synchronous psycopg2 connection if it uses cursor?
    # Checking AnexoRouter... it uses `repo = AnexoRepository(db_conn)`.
    # And AnexoRepository uses `AsyncSession`.
    # However, AnexoRouter type hint says `psycopg2.extensions.connection`.
    # This might be a legacy typing issue in the code, but if the Repo expects AsyncSession (which it does in our previous view), 
    # and conftest yields AsyncSession, it should match runtime object.
    # Python checks type hints statically. Runtime injection depends on 'get_db'.
    # Our conftest overrides 'get_db' with AsyncSession.
    # So if Repo accepts AsyncSession, it's fine.
    
    if r.status_code != 201:
        # If it fails, print details
        print(r.json())
        
    assert r.status_code == 201
    resp = r.json()
    assert resp["mensagem"] == "Upload realizado com sucesso"
    assert resp["anexo"]["nome_original"] == "teste.pdf"

@pytest.mark.asyncio
async def test_download_anexo_404(client, usuario_normal_token):
    r = await client.get("/anexos/9999/download", headers=usuario_normal_token)
    assert r.status_code == 404
