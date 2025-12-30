from app.models.gestao.local_model import Local

def test_local_initialization():
    """
    Testa a inicialização de um Local de Entrega.
    """
    nome_local = "Almoxarifado Central"
    rua = "Av. das Indústrias"
    num = "1000"
    bairro = "Distrito Industrial"
    
    local = Local(
        nome=nome_local,
        logradouro=rua,
        numero=num,
        bairro=bairro,
        ativo=True,
        is_deleted=False
    )

    assert local.nome == nome_local
    assert local.logradouro == rua
    assert local.numero == num
    assert local.ativo is True
    
    assert local.is_deleted is False

def test_local_nullable_fields():
    """
    Verifica se campos opcionais (complemento, cep, telefone) aceitam None.
    """
    local = Local(
        nome="Sede Administrativa",
        logradouro="Rua Principal",
        numero="1",
        bairro="Centro",
        complemento=None,
        cep=None,
        telefone_contato=None
    )
    
    assert local.complemento is None
    assert local.telefone_contato is None