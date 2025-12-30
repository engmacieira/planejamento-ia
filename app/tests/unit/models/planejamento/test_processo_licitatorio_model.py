from decimal import Decimal
from datetime import date
from app.models.planejamento.processo_licitatorio_model import ProcessoLicitatorio

def test_processo_licitatorio_initialization():
    """
    Testa a inicialização de um Processo Licitatório.
    """
    num_proc = 10
    ano = 2024
    obj = "Aquisição de Mobiliário Escolar"
    valor = Decimal("150000.00")
    status = "Publicado"
    
    dfd_id = 100
    mod_id = 1
    
    proc = ProcessoLicitatorio(
        id_dfd=dfd_id,
        numero_processo=num_proc,
        ano_processo=ano,
        id_modalidade=mod_id,
        objeto=obj,
        valor_total_estimado=valor,
        status=status,
        data_abertura=date.today(),
        is_deleted=False
    )

    assert proc.numero_processo == num_proc
    assert proc.objeto == obj
    assert proc.valor_total_estimado == valor
    assert proc.status == status
    assert proc.id_dfd == dfd_id
    
    assert proc.is_deleted is False

def test_processo_licitatorio_nullable():
    """
    Verifica campos opcionais.
    """
    proc = ProcessoLicitatorio(
        id_dfd=1,
        numero_processo=1,
        ano_processo=2024,
        id_modalidade=1,
        objeto="Teste",
        id_numero_modalidade=None,
        data_homologacao=None
    )
    
    assert proc.data_homologacao is None