from app.models.gestao.descricao_item_model import DescricaoItem

def test_descricao_item_initialization():
    """
    Testa a inicialização da Descrição do Item e herança.
    """
    texto = "Parafusos de fixação 10mm em aço inox com tratamento antiferrugem"
    
    desc = DescricaoItem(
        descricao=texto,
        is_deleted=False
    )

    assert desc.descricao == texto
    
    assert desc.is_deleted is False