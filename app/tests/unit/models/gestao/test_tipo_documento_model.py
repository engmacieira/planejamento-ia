from app.models.gestao.tipo_documento_model import TipoDocumento

def test_tipo_documento_initialization():
    """
    Testa a inicialização de um Tipo de Documento.
    """
    nome = "Parecer Técnico"
    desc = "Documento emitido por especialista"
    
    tipo = TipoDocumento(
        nome=nome,
        descricao=desc,
        ativo=True,
        is_deleted=False
    )

    assert tipo.nome == nome
    assert tipo.descricao == desc
    assert tipo.ativo is True
    
    assert tipo.is_deleted is False

def test_tipo_documento_nullable():
    """
    Verifica campos opcionais.
    """
    tipo = TipoDocumento(
        nome="Ofício",
        descricao=None
    )
    
    assert tipo.descricao is None