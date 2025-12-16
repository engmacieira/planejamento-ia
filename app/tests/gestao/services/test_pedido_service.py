import pytest
from app.services.gestao.pedido_service import PedidoService

@pytest.mark.asyncio
async def test_create_pedido_com_itens_placeholder(db_session):
    service = PedidoService()
    # It returns None currently as placeholder
    res = service.create_pedido_com_itens(db_session, None, [])
    assert res is None
