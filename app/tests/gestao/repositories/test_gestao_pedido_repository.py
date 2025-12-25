import pytest
from app.repositories.gestao.pedido_repository import PedidoRepository
from app.schemas.gestao.pedido_schema import PedidoCreateRequest
from datetime import date

@pytest.mark.asyncio
async def test_create_pedido_custom(db_session):
    repo = PedidoRepository(db_session)
    
    # Using generic IDs
    pedido_in = PedidoCreateRequest(
        id_contrato=1,
        id_item_contrato=1, # Field name check: schema has item_contrato_id? Repo handles mapping?
        # Let's use schema keys assuming Pydantic model dump works
        item_contrato_id=10, # Repo maps this to id_item_contrato
        quantidade=50.0,
        valor_unitario=10.0,
        valor_total=500.0,
        local_entrega="Local X",
        data_solicitacao=date.today(),
        prazo_entrega=5,
        observacoes="Teste"
    )
    
    try:
        # Custom method create_pedido(id_aocs, req)
        pedido = await repo.create_pedido(id_aocs=99, pedido_req=pedido_in)
        assert pedido.id is not None
        assert pedido.id_aocs == 99
        assert pedido.status_entrega == "Pendente"
        # Check mapping
        assert pedido.id_item_contrato == 10
    except Exception as e:
        pytest.fail(f"Failed to create pedido: {e}")
