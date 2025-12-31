from typing import TYPE_CHECKING, List
from sqlalchemy import String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.base_model import DefaultModel 

if TYPE_CHECKING:
    from app.models.core.user_model import User
    # from app.models.core.log_documento_model import GenerationLog 
    # (Descomente acima quando criar o log)

class Template(DefaultModel, Base): 
    """
    Cadastro de Templates (.docx) para geração de documentos.
    Armazena o caminho do arquivo físico e metadados sobre como preenchê-lo.
    """
    __tablename__ = "templates"

    # Identificação do Modelo
    nome: Mapped[str] = mapped_column(String(150), nullable=False, comment="Ex: Edital Pregão Eletrônico - Bens Comuns")
    descricao: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # Classificação (Para filtrar no frontend)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, comment="Ex: EDITAL, CONTRATO, ATA, TR, CAPA")
    
    # Arquivo Físico
    filename: Mapped[str] = mapped_column(String(255), nullable=False, comment="Nome original do arquivo .docx")
    path: Mapped[str] = mapped_column(String(500), nullable=False, comment="Caminho no disco ou S3")
    
    # Inteligência de Preenchimento
    # Aqui guardamos uma lista das variáveis que esse documento TEM que ter.
    # Ex: ["numero_processo", "data_abertura", "nome_pregoeiro"]
    # Isso ajuda o frontend a gerar o formulário dinâmico para o usuário.
    variaveis_esperadas: Mapped[List[str] | None] = mapped_column(JSON, nullable=True)
    
    # Controle
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Quem subiu o template? (Padronizado para 'responsavel_id')
    responsavel_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False) 
    responsavel: Mapped["User"] = relationship("User", lazy="selectin")
    
    # Logs de uso (Quantas vezes esse template foi usado?)
    # Mantive comentado para evitar erro de import se o arquivo log não existir ainda,
    # mas a estrutura está pronta.
    # logs: Mapped[List["GenerationLog"]] = relationship("GenerationLog", back_populates="template")

    def __repr__(self):
        return f"<Template '{self.nome}' ({self.tipo})>"