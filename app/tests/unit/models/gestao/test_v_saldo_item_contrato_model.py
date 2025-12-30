from decimal import Decimal
from app.models.gestao.v_saldo_item_contrato_model import VSaldoItemContrato

def test_v_saldo_instantiation():
    """
    Testa o mapeamento de tipos da View (Read-Only).
    """
    qtd = Decimal("100.000")
    consumido = Decimal("25.500")
    saldo = Decimal("74.500")
    
    view_row = VSaldoItemContrato(
        id_item_contrato=1,
        id_contrato=10,
        nome_item="Cimento CP-II",
        quantidade_contratada=qtd,
        total_consumido=consumido,
        saldo_disponivel=saldo
    )

    assert view_row.nome_item == "Cimento CP-II"
    assert view_row.saldo_disponivel == saldo
    assert isinstance(view_row.saldo_disponivel, Decimal)