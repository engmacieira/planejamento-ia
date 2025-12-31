from sqlalchemy import Column, String
from app.core.base_model import DefaultModel

class Orgao(DefaultModel):
    """
    Representa a Entidade Pública que utiliza o sistema (ex: Prefeitura Municipal de X).
    
    Regra de Negócio:
    - O sistema é desenhado para ser Mono-Órgão por instância de Banco de Dados.
    - Teoricamente, esta tabela deve conter apenas 1 registro ativo.
    - Seus dados são vitais para a geração automática de cabeçalhos em documentos (PDF/DOCX).
    """
    __tablename__ = "orgaos"

    # Identificação Principal
    nome = Column(String(255), nullable=False, comment="Nome oficial (ex: Prefeitura Municipal de Salvador)")
    cnpj = Column(String(14), unique=True, nullable=False, index=True, comment="CNPJ (apenas números)")
    sigla = Column(String(20), nullable=True, comment="Sigla do Órgão (ex: PMS)")
    
    # Endereço e Contato (Usados no Rodapé dos documentos)
    endereco = Column(String(255), nullable=True)
    cidade = Column(String(100), nullable=False, comment="Cidade sede")
    uf = Column(String(2), nullable=False, comment="Estado (UF)")
    cep = Column(String(8), nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    site = Column(String(255), nullable=True)
    
    # Identidade Visual
    logo_path = Column(String(255), nullable=True, comment="Caminho relativo para o arquivo de logo (usado em relatórios)")

    # Esfera Administrativa (Importante para regras da Lei 14.133)
    esfera = Column(String(20), default="Municipal", comment="Municipal, Estadual ou Federal")

    def __repr__(self):
        return f"<Orgao {self.nome} ({self.sigla})>"