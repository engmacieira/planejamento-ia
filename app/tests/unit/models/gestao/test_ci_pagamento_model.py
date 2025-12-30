from datetime import date
from decimal import Decimal
from app.models.gestao.ci_pagamento_model import CiPagamento

def test_ci_pagamento_initialization():
    """
    Testa a inicialização de uma CI de Pagamento.
    """
    num_ci = "CI-2024/999"
    valor = Decimal("1500.50")
    nf = "000123"
    hoje = date.today()
    aocs_id = 10
    
    ci = CiPagamento(
        numero_ci=num_ci,
        data_ci=hoje,
        id_aocs=aocs_id,
        numero_nota_fiscal=nf,
        data_nota_fiscal=hoje,
        valor_nota_fiscal=valor,
        is_deleted=False
    )

    assert ci.numero_ci == num_ci
    assert ci.valor_nota_fiscal == valor
    assert ci.id_aocs == aocs_id
    assert ci.is_deleted is False

def test_ci_pagamento_nullable_fields():
    """
    Verifica campos opcionais (série, código de acesso, observações).
    """
    ci = CiPagamento(
        numero_ci="CI-TEST",
        data_ci=date.today(),
        id_aocs=1,
        numero_nota_fiscal="123",
        data_nota_fiscal=date.today(),
        valor_nota_fiscal=Decimal("10.00"),
        serie_nota_fiscal=None,
        codigo_acesso_nota=None,
        observacoes=None
    )
    
    assert ci.serie_nota_fiscal is None
    assert ci.observacoes is None