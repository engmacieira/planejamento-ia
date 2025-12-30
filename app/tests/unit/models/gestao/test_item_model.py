from decimal import Decimal
from app.models.gestao.item_model import ItemContrato

def test_item_contrato_initialization():
    """
    Testa a inicialização de um Item de Contrato.
    """
    qtd = Decimal("10.500")
    valor_unit = Decimal("150.00")
    marca = "Dell"
    item_dfd_id = 500
    
    item = ItemContrato(
        id_contrato=1,
        id_item_dfd=item_dfd_id,
        numero_item=1,
        quantidade_contratada=qtd,
        valor_unitario_final=valor_unit,
        marca=marca,
        is_deleted=False
    )

    assert item.quantidade_contratada == qtd
    assert item.valor_unitario_final == valor_unit
    assert item.marca == marca
    assert item.id_item_dfd == item_dfd_id
    assert item.is_deleted is False
    
def test_item_contrato_nullable():
    """
    Verifica campos opcionais.
    """
    item = ItemContrato(
        id_contrato=1,
        id_item_dfd=1,
        numero_item=2,
        quantidade_contratada=Decimal("1"),
        valor_unitario_final=Decimal("10"),
        marca=None
    )
    
    assert item.marca is None