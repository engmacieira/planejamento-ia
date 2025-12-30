from app.models.core.agente_model import Agente

from app.models.core.agente_model import Agente

def test_agente_model_initialization():
    """
    Testa a inicialização do Agente e a herança do DefaultModel.
    """
    nome = "James Bond"
    cpf = "00700700707"
    email = "007@mi6.com"
    cargo = "Espião"
    
    agente = Agente(
        nome=nome,
        cpf=cpf,
        email=email,
        cargo=cargo,
        ativo=True, 
        is_deleted=False
    )

    assert agente.nome == nome
    assert agente.cpf == cpf
    assert agente.cargo == cargo
    
    assert agente.ativo is True  
    assert agente.is_deleted is False
    assert agente.email == email

def test_agente_nullable_fields():
    """
    Verifica se campos opcionais aceitam None.
    """
    agente = Agente(
        nome="Recruta Zero",
        cpf="11111111111",
        matricula=None,
        telefone=None
    )
    
    assert agente.matricula is None
    assert agente.telefone is None