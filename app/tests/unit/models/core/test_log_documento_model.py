from app.models.core.log_documento_model import GenerationLog

def test_generation_log_initialization():
    """
    Testa a inicialização do Log de Geração de Documentos e a herança.
    """
    # Arrange
    filename = "edital_concluido_v1.docx"
    user_id = 42
    template_id = 10
    
    # Act
    log = GenerationLog(
        generated_filename=filename,
        user_id=user_id,
        template_id=template_id,
        # Default explícito para teste em memória
        is_deleted=False
    )

    # Assert
    assert log.generated_filename == filename
    assert log.user_id == user_id
    assert log.template_id == template_id
    
    # Testando herança
    assert log.is_deleted is False

def test_generation_log_relationships_ids():
    """
    Verifica se as Foreign Keys estão sendo atribuídas corretamente.
    (Teste de estrutura, não de integridade referencial de banco).
    """
    log = GenerationLog(
        user_id=99,
        template_id=50
    )
    
    assert log.user_id == 99
    assert log.template_id == 50