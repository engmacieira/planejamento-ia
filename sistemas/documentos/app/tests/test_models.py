import pytest
from sqlalchemy.exc import IntegrityError
from app.models import User, Template, GenerationLog

def test_user_creation_and_default_fields(db_session):
    """
    Testa se cria o usuário e se a herança do DefaultModel 
    (created_at, is_deleted) está funcionando.
    """
    # 1. Cria um usuário simples
    user = User(name="Matheus Teste", email="teste@models.com", password_hash="hash123")
    db_session.add(user)
    db_session.commit()
    
    # 2. Verifica se foi salvo e gerou ID
    assert user.id is not None
    assert user.name == "Matheus Teste"
    
    # 3. Verifica os campos do DefaultModel (Core)
    assert user.created_at is not None
    assert user.is_deleted is False

def test_user_unique_email_constraint(db_session):
    """
    Testa se o banco BLOQUEIA emails duplicados.
    Isso é crucial para a integridade do sistema.
    """
    # 1. Cria o primeiro usuário
    user1 = User(name="User 1", email="unico@email.com", password_hash="123")
    db_session.add(user1)
    db_session.commit()

    # 2. Tenta criar o segundo com MESMO email
    user2 = User(name="User 2", email="unico@email.com", password_hash="456")
    db_session.add(user2)

    # 3. Esperamos que o SQLAlchemy levante um erro de Integridade
    with pytest.raises(IntegrityError):
        db_session.commit()
    
    # Limpa a sessão para não travar os próximos testes (rollback obrigatório após erro)
    db_session.rollback()

def test_relationships(db_session):
    """
    Testa se User, Template e Log estão conversando entre si.
    """
    # 1. Cria o Dono (User)
    owner = User(name="Dono", email="dono@email.com", password_hash="123")
    db_session.add(owner)
    db_session.commit()

    # 2. Cria o Template ligado ao Dono
    template = Template(
        filename="contrato.docx", 
        path="/tmp/contrato.docx", 
        owner_id=owner.id
    )
    db_session.add(template)
    db_session.commit()

    # 3. Verifica se o relacionamento funcionou (acessando .owner pelo template)
    assert template.owner.name == "Dono"
    
    # 4. Verifica o caminho inverso (acessando .templates pelo user)
    # O user deve ter 1 template na lista
    assert len(owner.templates) == 1
    assert owner.templates[0].filename == "contrato.docx"