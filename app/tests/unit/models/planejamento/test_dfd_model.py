from datetime import date
from app.models.planejamento.dfd_model import DFD

def test_dfd_initialization():
    """
    Testa a inicialização do Documento de Formalização da Demanda.
    """
    numero = 1
    ano = 2024
    desc = "Aquisição de computadores"
    unidade_id = 55
    resp_id = 10
    hoje = date.today()
    
    dfd = DFD(
        numero=numero,
        ano=ano,
        descricao_sucinta=desc,
        unidade_requisitante_id=unidade_id,
        responsavel_id=resp_id,
        data_req=hoje,
        status="Rascunho",
        ativo=True,
        is_deleted=False
    )

    assert dfd.numero == numero
    assert dfd.descricao_sucinta == desc
    assert dfd.status == "Rascunho"
    assert dfd.ativo is True
    
    assert dfd.is_deleted is False

def test_dfd_nullable_fields():
    """
    Verifica campos opcionais do DFD.
    """
    dfd = DFD(
        numero=2,
        ano=2024,
        descricao_sucinta="Teste",
        unidade_requisitante_id=1,
        responsavel_id=1,
        data_req=date.today(),
        justificativa_necessidade=None,
        numero_protocolo_string=None,
        etp_id=None
    )
    
    assert dfd.justificativa_necessidade is None
    assert dfd.etp_id is None