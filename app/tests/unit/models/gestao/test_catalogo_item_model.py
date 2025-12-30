from app.models.gestao.catalogo_item_model import CatalogoItem

def test_catalogo_item_initialization():
    """
    Testa a inicialização de um Item do Catálogo.
    """
    nome = "Notebook I7 16GB"
    unidade = "UN"
    tipo = "Material"
    subgrupo_id = 5
    taxonomia = "0001"
    
    item = CatalogoItem(
        nome_item=nome,
        unidade_medida=unidade,
        tipo=tipo,
        id_subgrupo=subgrupo_id,
        numero_sequencial_taxonomia=taxonomia,
        ativo=True,
        is_deleted=False
    )

    assert item.nome_item == nome
    assert item.id_subgrupo == subgrupo_id
    assert item.numero_sequencial_taxonomia == taxonomia
    assert item.ativo is True
    
    assert item.is_deleted is False

def test_catalogo_item_nullable_fields():
    """
    Verifica se campos opcionais (códigos, descrição) aceitam None.
    """
    item = CatalogoItem(
        nome_item="Serviço de Limpeza",
        unidade_medida="SV",
        tipo="Serviço",
        id_subgrupo=2,
        numero_sequencial_taxonomia="0002",
        codigo_catmat_catser=None,
        descricao_detalhada=None
    )
    
    assert item.codigo_catmat_catser is None
    assert item.descricao_detalhada is None