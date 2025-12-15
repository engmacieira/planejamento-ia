from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, BigInteger, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class TipoDocumento(Base):
    __tablename__ = "tipos_documento"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    anexos = relationship("Anexo", back_populates="tipo_documento")


class Anexo(Base):
    __tablename__ = "anexos"

    id = Column(Integer, primary_key=True, index=True)
    nome_original = Column(String(255), nullable=False)
    nome_seguro = Column(String(255), unique=True, nullable=False)
    caminho_arquivo = Column(String(500))
    tamanho_bytes = Column(BigInteger)
    mimetype = Column(String(100))
    
    id_tipo_documento = Column(Integer, ForeignKey("tipos_documento.id"))
    
    id_contrato = Column(Integer, ForeignKey("contratos.id", ondelete="CASCADE"), nullable=True)
    id_aocs = Column(Integer, ForeignKey("aocs.id", ondelete="CASCADE"), nullable=True)
    
    data_upload = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "(id_contrato IS NOT NULL AND id_aocs IS NULL) OR (id_contrato IS NULL AND id_aocs IS NOT NULL)",
            name='check_origem_anexo'
        ),
    )

    tipo_documento = relationship("TipoDocumento", back_populates="anexos")
    
    # Relationships with other modules (using string to avoid circular deps if needed, but best if loaded)
    contrato = relationship("Contrato", back_populates="anexos") # Needs to be added to Contrato
    aocs = relationship("AOCS", back_populates="anexos") # Needs to be added to AOCS
