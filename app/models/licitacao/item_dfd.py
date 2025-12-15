from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class ItemDFD(Base):
    __tablename__ = "itens_dfd"

    id = Column(Integer, primary_key=True, index=True)
    id_dfd = Column(Integer, ForeignKey("dfd.id", ondelete="CASCADE"), nullable=False)
    id_catalogo_item = Column(Integer, ForeignKey("catalogo_itens.id"), nullable=False)
    
    numero_item = Column(Integer, nullable=False)
    quantidade = Column(Numeric(15, 3), nullable=False)
    valor_unitario_estimado = Column(Numeric(15, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint('id_dfd', 'id_catalogo_item', name='uk_item_dfd'),
    )

    dfd = relationship("app.models.licitacao.dfd.DFD", back_populates="itens")
    catalogo_item = relationship("app.models.catalogo.CatalogoItem") 
