from decimal import Decimal
from app.models.planejamento.item_etp_model import ItemETP

def test_item_etp_initialization():
    """
    Testa a inicialização de um Item do ETP.
    """
    qtd = Decimal("100.000")
    valor_ref = Decimal("50.00")
    valor_tot = Decimal("5000.00")
    etp_id = 10
    cat_id = 55
    
    item = ItemETP(
        etp_id=etp_id,
        catalogo_item_id=cat_id,
        quantidade_total=qtd,
        valor_unitario_referencia=valor_ref,
        valor_total_estimado=valor_tot,
        is_deleted=False
    )

    assert item.quantidade_total == qtd
    assert item.valor_unitario_referencia == valor_ref
    assert item.valor_total_estimado == valor_tot
    assert item.catalogo_item_id == cat_id
    
    assert item.is_deleted is False

def test_item_etp_nullable_fields():
    """
    Verifica se campos numéricos opcionais aceitam None.
    """
    item = ItemETP(
        etp_id=1,
        quantidade_total=None
    )
    
    assert item.quantidade_total is None