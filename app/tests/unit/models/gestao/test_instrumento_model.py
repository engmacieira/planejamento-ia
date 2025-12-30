from app.models.gestao.instrumento_model import InstrumentoContratual

def test_instrumento_initialization():
    """
    Testa a inicialização do Instrumento Contratual.
    """
    nome = "Ata de Registro de Preços"
    
    instrumento = InstrumentoContratual(
        nome=nome,
        ativo=True,
        is_deleted=False
    )

    assert instrumento.nome == nome
    assert instrumento.ativo is True
    
    assert instrumento.is_deleted is False