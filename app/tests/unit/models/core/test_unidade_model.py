from app.models.core.unidade_model import Unidade

def test_unidade_initialization():
    """
    Testa a inicialização da Unidade e a herança.
    """
    nome = "Secretaria de Tecnologia"
    sigla = "SETEC"
    
    unidade = Unidade(
        nome=nome,
        sigla=sigla,
        ativo=True,
        is_deleted=False
    )

    assert unidade.nome == nome
    assert unidade.sigla == sigla
    assert unidade.ativo is True
    assert unidade.is_deleted is False

def test_unidade_hierarquia():
    """
    Simula uma relação Pai-Filho (Departamento -> Setor).
    Em teste unitário (sem banco), validamos apenas a atribuição dos IDs.
    """
    id_pai = 10
    
    filha = Unidade(
        nome="Divisão de Infraestrutura",
        id_unidade_pai=id_pai,
        ativo=True,
        is_deleted=False
    )
    
    assert filha.id_unidade_pai == id_pai