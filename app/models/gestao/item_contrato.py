from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Numeric, UniqueConstraint, CheckConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class ItemContrato(Base):
    __tablename__ = "itens_contrato"

    id = Column(Integer, primary_key=True, index=True)
    id_contrato = Column(Integer, ForeignKey("contratos.id", ondelete="CASCADE"), nullable=False)
    id_item_dfd = Column(Integer, ForeignKey("itens_dfd.id"), nullable=False)
    
    numero_item = Column(Integer, nullable=False)
    marca = Column(String(150))
    
    quantidade_contratada = Column(Numeric(15, 3), nullable=False)
    valor_unitario_final = Column(Numeric(15, 2), nullable=False)
    
    ativo = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('id_contrato', 'numero_item', name='uk_item_numero_contrato'),
        UniqueConstraint('id_contrato', 'id_item_dfd', name='uk_item_origem_duplicada'),
    )

    contrato = relationship("app.models.gestao.contrato.Contrato", back_populates="itens")
    item_dfd = relationship("app.models.licitacao.item_dfd.ItemDFD")
