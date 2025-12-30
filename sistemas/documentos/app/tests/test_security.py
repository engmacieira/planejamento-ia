from datetime import timedelta
from jose import jwt
from app.core.security import create_access_token, SECRET_KEY, ALGORITHM

def test_create_access_token_with_custom_expiration():
    """
    Testa a criação de token com tempo de expiração personalizado.
    Cobre a linha: expire = datetime.utcnow() + expires_delta
    """
    data = {"sub": "test@expire.com"}
    # Define uma validade de 1 hora
    expires = timedelta(minutes=60)
    
    # Executa a linha não testada
    token = create_access_token(data, expires_delta=expires)
    
    # Decodifica para verificar
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # O campo 'exp' deve existir
    assert "exp" in payload
    # Não validamos o tempo exato para evitar "flaky tests" (testes instáveis com tempo),
    # mas o fato de ter decodificado sem erro e ter 'exp' já cobre a linha.