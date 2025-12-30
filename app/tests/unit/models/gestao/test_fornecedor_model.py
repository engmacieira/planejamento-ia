from app.models.gestao.fornecedor_model import Fornecedor

def test_fornecedor_initialization():
    """
    Testa a inicialização de um Fornecedor e herança.
    """
    razao = "Acme Corp Ltda"
    fantasia = "Loja do Coiote"
    cnpj = "12.345.678/0001-90"
    email = "contato@acme.com"
    
    fornecedor = Fornecedor(
        razao_social=razao,
        nome_fantasia=fantasia,
        cpf_cnpj=cnpj,
        email=email,
        ativo=True,
        is_deleted=False
    )

    assert fornecedor.razao_social == razao
    assert fornecedor.nome_fantasia == fantasia
    assert fornecedor.cpf_cnpj == cnpj
    assert fornecedor.ativo is True
    
    assert fornecedor.is_deleted is False

def test_fornecedor_nullable_fields():
    """
    Verifica se campos opcionais aceitam None.
    """
    fornecedor = Fornecedor(
        razao_social="Empresa Simples",
        cpf_cnpj="11122233344",
        nome_fantasia=None,
        telefone=None,
        email=None
    )
    
    assert fornecedor.nome_fantasia is None
    assert fornecedor.telefone is None
    assert fornecedor.email is None