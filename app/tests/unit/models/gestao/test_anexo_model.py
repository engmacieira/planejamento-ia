from app.models.gestao.anexo_model import Anexo

def test_anexo_model_initialization():
    """
    Testa a inicialização básica de um Anexo e herança do DefaultModel.
    """
    nome_orig = "contrato_assinado.pdf"
    nome_seg = "20231020_contrato_uuid.pdf"
    mime = "application/pdf"
    
    anexo = Anexo(
        nome_original=nome_orig,
        nome_seguro=nome_seg,
        mimetype=mime,
        id_contrato=10, 
        is_deleted=False
    )

    assert anexo.nome_original == nome_orig
    assert anexo.id_contrato == 10
    assert anexo.id_aocs is None  
    
    assert anexo.is_deleted is False

def test_anexo_polymorphism_fields():
    """
    Verifica se conseguimos instanciar focando na outra ponta (AOCS).
    Nota: A validação de EXCLUSIVIDADE (CheckConstraint) só ocorre no banco real,
    não aqui na memória. Aqui testamos apenas se os campos aceitam os valores.
    """
    anexo = Anexo(
        nome_original="nota_fiscal.xml",
        nome_seguro="nf_123.xml",
        id_aocs=55,
        is_deleted=False
    )
    
    assert anexo.id_aocs == 55
    assert anexo.id_contrato is None