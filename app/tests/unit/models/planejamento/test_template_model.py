from app.models.planejamento.template_model import Template

def test_template_initialization():
    """
    Testa a inicialização de um Template de documento.
    """
    fname = "modelo_contrato_2024.docx"
    fpath = "/storage/templates/v1/contrato.docx"
    desc = "Minuta padrão de contrato de serviços"
    owner_id = 1
    
    tpl = Template(
        filename=fname,
        path=fpath,
        description=desc,
        owner_id=owner_id,
        # DefaultModel
        is_deleted=False
    )

    assert tpl.filename == fname
    assert tpl.path == fpath
    assert tpl.description == desc
    assert tpl.owner_id == owner_id
    
    assert tpl.is_deleted is False

def test_template_nullable_fields():
    """
    Verifica campos opcionais.
    """
    tpl = Template(
        filename="teste.docx",
        path="/tmp/teste.docx",
        owner_id=1,
        description=None
    )
    
    assert tpl.description is None