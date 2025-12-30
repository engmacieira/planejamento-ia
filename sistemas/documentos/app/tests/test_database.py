from app.core.database import get_db, SessionLocal

def test_get_db():
    """
    Testa se o gerador de dependência consegue entregar uma sessão válida.
    """
    # 1. Pega o gerador
    generator = get_db()
    
    # 2. Avança para o primeiro yield (pega a sessão)
    db_session = next(generator)
    
    # 3. Verifica se é uma sessão válida do SQLAlchemy
    # (Não verificamos se conecta no banco real, apenas se o objeto foi criado)
    assert db_session is not None
    
    # 4. Simula o fim do uso (para cair no 'finally: db.close()')
    try:
        next(generator)
    except StopIteration:
        pass # É esperado que o gerador acabe aqui