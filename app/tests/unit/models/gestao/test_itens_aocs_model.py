from decimal import Decimal
from app.models.gestao.itens_aocs_model import ItensAocs

def test_itens_aocs_initialization():
    """
    Testa a inicialização de um Item dentro de uma AOCS.
    """
    qtd_solicitada = Decimal("100.000")
    saldo_snapshot = Decimal("500.000")
    aocs_id = 10
    item_contrato_id = 55
    
    item = ItensAocs(
        id_aocs=aocs_id,
        id_item_contrato=item_contrato_id,
        quantidade_solicitada=qtd_solicitada,
        saldo_anterior_snapshot=saldo_snapshot,
        is_deleted=False
    )

    assert item.quantidade_solicitada == qtd_solicitada
    assert item.saldo_anterior_snapshot == saldo_snapshot
    assert item.id_aocs == aocs_id
    
    assert item.status_item == 'Aguardando Entrega' or item.status_item is None 
    
    assert item.is_deleted is False

def test_itens_aocs_defaults_update():
    """
    Verifica a atualização de status e entrega.
    """
    item = ItensAocs(
        quantidade_solicitada=Decimal("50.000"),
        quantidade_entregue=Decimal("50.000"),
        status_item="Entregue Totalmente"
    )
    
    assert item.quantidade_entregue == Decimal("50.000")
    assert item.status_item == "Entregue Totalmente"