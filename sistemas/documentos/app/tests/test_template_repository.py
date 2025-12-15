import pytest
from unittest.mock import patch
from app.repositories.template_repository import TemplateRepository
from app.models.user_model import User
from app.schemas.template_schema import TemplateCreate

# --- FIXTURES (Preparação) ---
@pytest.fixture
def owner(db_session):
    """Cria um usuário dono para os testes."""
    user = User(name="Dono", email="dono@template.com", password_hash="123")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# --- TESTES ---

def test_template_lifecycle(db_session, owner):
    """
    Testa o ciclo normal: Criar -> Listar -> Deletar.
    """
    # 1. Definindo 'repo' (Crucial para não dar erro de undefined)
    repo = TemplateRepository(db_session)
    
    # 2. Definindo 'data'
    data = TemplateCreate(filename="minuta_vendas.docx", description="Para vendas")
    
    # Ação
    template = repo.create(data, saved_path="/tmp/uploads/minuta.docx", owner_id=owner.id)
    
    # Asserts
    assert template.id is not None
    assert template.is_deleted is False

    # Soft Delete
    repo.delete(template.id)
    deleted_template = repo.get_by_id(template.id)
    assert deleted_template.is_deleted is True

def test_create_template_error(db_session):
    """
    Testa erro na criação (FK inválida).
    """
    # 1. Definindo 'repo' NOVAMENTE (novo escopo)
    repo = TemplateRepository(db_session)
    
    # 2. Definindo 'data' NOVAMENTE
    data = TemplateCreate(filename="fail.docx", description="fail")
    
    # Ação: Tenta criar com owner_id 9999 (inexistente)
    with pytest.raises(Exception):
        repo.create(data, saved_path="/path/falso", owner_id=9999)

def test_delete_template_error(db_session, owner):
    """
    Testa erro no delete (Simulado com Mock).
    """
    # 1. Definindo 'repo'
    repo = TemplateRepository(db_session)
    
    # 2. Criando um template real para poder tentar deletar
    data = TemplateCreate(filename="delete_fail.docx")
    template = repo.create(data, saved_path="/path", owner_id=owner.id)

    # 3. Mockando o commit para falhar
    with patch.object(db_session, 'commit', side_effect=Exception("Erro Forçado no Commit")):
        with pytest.raises(Exception) as excinfo:
            repo.delete(template.id)
        
        # Verifica se a mensagem de erro bate com a do Mock
        assert "Erro Forçado no Commit" in str(excinfo.value)
        
def test_list_templates_filtering_logic(db_session):
    """
    Testa a 'peneira' do list_by_user.
    Cenário:
    - User A tem um template ativo.
    - User A tem um template deletado (Soft Delete).
    - User B tem um template ativo.
    
    Resultado esperado ao listar User A: Apenas o template ativo do User A.
    """
    repo = TemplateRepository(db_session)
    
    # 1. Cria User A e User B
    user_a = User(name="User A", email="a@filter.com", password_hash="123")
    user_b = User(name="User B", email="b@filter.com", password_hash="123")
    db_session.add_all([user_a, user_b])
    db_session.commit()
    
    # 2. Popula o Banco
    # Template do A (Ativo) -> DEVE VIR
    t_a_active = repo.create(
        TemplateCreate(filename="a_ativo.docx"), "/path", user_a.id
    )
    
    # Template do A (Deletado) -> NÃO DEVE VIR
    t_a_deleted = repo.create(
        TemplateCreate(filename="a_deleted.docx"), "/path", user_a.id
    )
    repo.delete(t_a_deleted.id) # Deleta ele
    
    # Template do B (Ativo) -> NÃO DEVE VIR (Pertence a outro)
    t_b_active = repo.create(
        TemplateCreate(filename="b_ativo.docx"), "/path", user_b.id
    )
    
    # 3. Executa a listagem focada no User A
    # AQUI a linha do filtro será testada ao máximo
    result_list = repo.list_by_user(user_a.id)
    
    # 4. Verificações
    assert len(result_list) == 1
    assert result_list[0].id == t_a_active.id
    assert result_list[0].filename == "a_ativo.docx"