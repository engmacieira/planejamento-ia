from datetime import date
from app.models.gestao.aocs_model import Aocs

def test_aocs_model_initialization():
    """
    Testa a inicialização de uma AOCS com todos os campos recuperados.
    """
    numero = "001/2024"
    ano = 2024
    unidade_id = 55
    pedido_ext = "PED-1234"
    
    aocs = Aocs(
        numero_aocs=numero,
        ano_aocs=ano,
        id_unidade_requisitante=unidade_id, 
        numero_pedido_externo=pedido_ext,
        status="Emitida",
        is_deleted=False
    )

    assert aocs.numero_aocs == numero
    assert aocs.id_unidade_requisitante == unidade_id
    assert aocs.numero_pedido_externo == pedido_ext
    assert aocs.is_deleted is False

def test_aocs_nullable_fields():
    """
    Verifica se campos opcionais aceitam None.
    """
    aocs = Aocs(
        numero_aocs="002/2024",
        ano_aocs=2024,
        id_unidade_requisitante=1,
        numero_pedido_externo=None,
        empenho=None,
        justificativa=None
    )
    
    assert aocs.numero_pedido_externo is None
    assert aocs.empenho is None