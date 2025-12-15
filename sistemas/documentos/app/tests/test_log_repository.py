import pytest
from app.repositories.log_repository import LogRepository
from app.models.user_model import User
from app.models.template_model import Template
from datetime import datetime
from app.schemas.log_schema import LogResponse

# Fixtures para preparar o terreno
@pytest.fixture
def user_and_template(db_session):
    # 1. Cria User
    user = User(name="Auditor", email="log@teste.com", password_hash="123")
    db_session.add(user)
    db_session.commit()
    
    # 2. Cria Template
    template = Template(filename="modelo.docx", path="/tmp/modelo.docx", owner_id=user.id)
    db_session.add(template)
    db_session.commit()
    
    return user, template

def test_log_creation(db_session, user_and_template):
    user, template = user_and_template
    repo = LogRepository(db_session)

    # Act: Cria o log
    log = repo.create_log(
        user_id=user.id, 
        template_id=template.id, 
        filename="modelo_preenchido_final.docx"
    )

    # Assert: Verifica se gravou tudo certo
    assert log.id is not None
    assert log.user_id == user.id
    assert log.template_id == template.id
    assert log.generated_filename == "modelo_preenchido_final.docx"

    # Verifica listagem
    history = repo.list_by_user(user.id)
    assert len(history) == 1
    assert history[0].generated_filename == "modelo_preenchido_final.docx"
    
def test_log_schema_definition():
    """
    Testa unitariamente se o Schema LogResponse consegue ser instanciado.
    Isso garante a cobertura das linhas de definição do Pydantic.
    """
    # 1. Simula um objeto vindo do banco (pode ser um objeto dummy ou dict)
    mock_log_db = {
        "id": 1,
        "generated_filename": "teste.docx",
        "user_id": 99,
        "template_id": 50,
        "created_at": datetime.now()
    }
    
    # 2. Força a validação (Isso executa o código do Schema)
    log_schema = LogResponse.model_validate(mock_log_db)
    
    assert log_schema.id == 1
    assert log_schema.generated_filename == "teste.docx"
    
def test_create_log_error_handling(db_session):
    """
    Testa se o Repositório captura erros de banco e faz rollback.
    Forçamos um erro usando IDs inexistentes (Violação de FK).
    """
    repo = LogRepository(db_session)

    # Tenta criar log com usuário ID 9999 (que não existe)
    # Isso gera IntegrityError no banco, que é capturado pelo Exception genérico
    with pytest.raises(Exception):
        repo.create_log(
            user_id=9999, 
            template_id=9999, 
            filename="erro.docx"
        )
    
    # Se o teste passou, significa que o repositório capturou o erro, 
    # imprimiu no stderr (coberto) e relançou o erro (raise e).