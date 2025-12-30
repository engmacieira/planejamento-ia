import pytest
from app.schemas.user_schema import UserCreate
from app.repositories.user_repository import UserRepository

def test_create_user_success(db_session):
    """
    Testa o Caminho Feliz: Criar um usuário corretamente.
    Valida se o ID é gerado, se os dados batem e se a senha não é salva pura.
    """
    # 1. Arrange (Prepara os dados)
    user_data = UserCreate(
        name="Matheus Dev",
        email="matheus@repository.com",
        password="senhasupersecreta"
    )
    
    # Instancia o repositório passando a sessão de teste
    repo = UserRepository(db_session)

    # 2. Act (Executa a função do repositório)
    created_user = repo.create_user(user_data)

    # 3. Assert (Verifica o resultado)
    assert created_user.id is not None          # Tem que ter ganhado um ID do banco
    assert created_user.name == user_data.name  # Nome tem que bater
    assert created_user.email == user_data.email # Email tem que bater
    assert created_user.is_deleted is False     # Não pode nascer deletado
    
    # Verifica segurança: a senha salva NÃO pode ser igual a senha plana
    assert created_user.password_hash != "senhasupersecreta" 

def test_create_user_duplicate_email_fail(db_session):
    """
    Testa o Caminho Triste: Tentar criar email duplicado deve falhar.
    Isso cobre o bloco 'except' e o 'rollback' do repositório.
    """
    # 1. Cria o primeiro usuário
    user_data = UserCreate(name="User 1", email="duplo@email.com", password="123")
    repo = UserRepository(db_session)
    repo.create_user(user_data)

    # 2. Tenta criar o segundo com MESMO email
    # O Repository captura o IntegrityError, faz rollback e re-lança como Exception genérica.
    with pytest.raises(Exception):
        repo.create_user(user_data)

def test_get_user_by_email(db_session):
    """
    Testa a busca de usuário por email.
    Cobre a linha: return self.db.query(User).filter(User.email == email).first()
    """
    repo = UserRepository(db_session)
    target_email = "findme@test.com"

    # 1. Cenário: Usuário não existe ainda
    # A função deve retornar None (e não dar erro)
    result_none = repo.get_by_email(target_email)
    assert result_none is None

    # 2. Cenário: Usuário existe
    # Criamos o usuário primeiro para poder buscar
    user_data = UserCreate(name="Escondido", email=target_email, password="123")
    repo.create_user(user_data)

    # Agora buscamos novamente
    result_found = repo.get_by_email(target_email)
    
    # Validações
    assert result_found is not None
    assert result_found.email == target_email
    assert result_found.name == "Escondido"