from app.models.core.log_auditoria_model import LogAuditoria

def test_log_auditoria_initialization():
    """
    Testa a inicialização de um Log de Auditoria, focando no suporte a JSON
    e na herança do DefaultModel.
    """
    tabela = "contratos"
    acao = "UPDATE"
    dados_velhos = {"valor": 1000, "status": "rascunho"}
    dados_novos = {"valor": 1200, "status": "ativo"}
    
    log = LogAuditoria(
        tabela_afetada=tabela,
        tipo_acao=acao,
        dados_antigos=dados_velhos,
        dados_novos=dados_novos,
        username_snapshot="admin_user",
        is_deleted=False
    )

    assert log.tabela_afetada == tabela
    assert log.tipo_acao == acao
    
    assert log.dados_antigos == dados_velhos
    assert log.dados_novos == dados_novos
    assert log.dados_antigos["valor"] == 1000
    
    assert log.is_deleted is False

def test_log_auditoria_nullable_json():
    """
    Garante que podemos criar logs sem dados detalhados (ex: DELETE sem dados novos).
    """
    log = LogAuditoria(
        tabela_afetada="usuarios",
        tipo_acao="DELETE",
        dados_antigos={"id": 1, "nome": "User Deletado"},
        dados_novos=None, 
        is_deleted=False
    )
    
    assert log.dados_novos is None
    assert log.dados_antigos is not None