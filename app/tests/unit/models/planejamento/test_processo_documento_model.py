from datetime import date
from app.models.planejamento.processo_documento_model import ProcessoDocumento
from app.models.planejamento.dfd_model import DFD

def test_processo_documento_integration():
    """
    Testa se o ProcessoDocumento se vincula corretamente a um DFD
    e armazena seus campos manuais.
    """
    dfd_mock = DFD(
        id=100,
        numero=123,
        ano=2024,
        descricao_sucinta="Aquisição de Veículos",
        unidade_requisitante_id=5,
        responsavel_id=1,
        data_req=date.today()
    )
    
    artigo_lei = "Art. 75, inciso II"
    dt_portaria = "15/03/2024"
    
    processo = ProcessoDocumento(
        dfd_id=100,     
        dfd=dfd_mock,    
        artigo=artigo_lei,
        data1=dt_portaria,
        owner_id=1,
        is_deleted=False
    )

    assert processo.artigo == artigo_lei
    assert processo.data1 == dt_portaria
    
    assert processo.dfd_id == 100
    assert processo.dfd.descricao_sucinta == "Aquisição de Veículos"
    
    assert processo.objeto == "Aquisição de Veículos"