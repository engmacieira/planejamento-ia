from decimal import Decimal
from datetime import date
from app.models.gestao.pedido_model import Pedido

def test_pedido_initialization():
    """
    Testa a inicialização de um Pedido de entrega.
    """
    qtd_pedida = Decimal("50.00")
    qtd_entregue = Decimal("0.00")
    hoje = date.today()
    status = "Pendente"
    item_legacy_id = 999
    
    pedido = Pedido(
        id_item_contrato=item_legacy_id,
        id_aocs=10,
        quantidade_pedida=qtd_pedida,
        data_pedido=hoje,
        status_entrega=status,
        quantidade_entregue=qtd_entregue,
        is_deleted=False
    )

    assert pedido.quantidade_pedida == qtd_pedida
    assert pedido.status_entrega == status
    assert pedido.id_item_contrato == item_legacy_id
    
    assert pedido.is_deleted is False