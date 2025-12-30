from decimal import Decimal
from app.models.planejamento.item_dfd_model import ItemDFD

def test_item_dfd_initialization():
    """
    Testa a inicialização de um Item do DFD.
    """
    qtd = Decimal("100.000")
    valor_unit = Decimal("50.00")
    complemento = "Cor azul marinho"
    dfd_id = 1
    cat_id = 500
    
    item = ItemDFD(
        dfd_id=dfd_id,
        catalogo_item_id=cat_id,
        numero_item=1,
        quantidade=qtd,
        valor_unitario_estimado=valor_unit,
        complemento_descricao=complemento,
        # DefaultModel
        is_deleted=False
    )

    assert item.quantidade == qtd
    assert item.valor_unitario_estimado == valor_unit
    assert item.complemento_descricao == complemento
    assert item.catalogo_item_id == cat_id
    
    assert item.is_deleted is False

def test_item_dfd_nullable():
    """
    Verifica campos opcionais.
    """
    item = ItemDFD(
        dfd_id=1,
        catalogo_item_id=1,
        numero_item=1,
        quantidade=Decimal("1"),
        valor_unitario_estimado=Decimal("1"),
        complemento_descricao=None
    )
    
    assert item.complemento_descricao is None