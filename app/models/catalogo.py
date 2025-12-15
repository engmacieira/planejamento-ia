from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), unique=True, nullable=False)
    codigo_taxonomia = Column(String(2), unique=True, nullable=False)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    grupos = relationship("Grupo", back_populates="categoria")


class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    id_categoria = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    codigo = Column(String(2), nullable=False)
    nome = Column(String(150), nullable=False)
    ativo = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('id_categoria', 'codigo', name='uk_grupo_codigo'),
    )

    categoria = relationship("Categoria", back_populates="grupos")
    subgrupos = relationship("Subgrupo", back_populates="grupo")


class Subgrupo(Base):
    __tablename__ = "subgrupos"

    id = Column(Integer, primary_key=True, index=True)
    id_grupo = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    codigo = Column(String(2), nullable=False)
    nome = Column(String(150), nullable=False)
    ativo = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('id_grupo', 'codigo', name='uk_subgrupo_codigo'),
    )

    grupo = relationship("Grupo", back_populates="subgrupos")
    itens = relationship("CatalogoItem", back_populates="subgrupo")


class CatalogoItem(Base):
    __tablename__ = "catalogo_itens"

    id = Column(Integer, primary_key=True, index=True)
    id_subgrupo = Column(Integer, ForeignKey("subgrupos.id"), nullable=False)
    
    nome_item = Column(String(255), nullable=False)
    unidade_medida = Column(String(50), nullable=False)
    tipo = Column(String(20), nullable=False) # Check constraint below
    
    codigo_catmat_catser = Column(String(50))
    numero_sequencial_taxonomia = Column(String(4), nullable=False)
    codigo_identificacao_completo = Column(String(10), unique=True)
    
    descricao_detalhada = Column(Text)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("tipo IN ('Consumo', 'Permanente', 'Serviço')", name='check_tipo_item'),
        UniqueConstraint('id_subgrupo', 'numero_sequencial_taxonomia', name='uk_item_sequencial'),
    )

    subgrupo = relationship("Subgrupo", back_populates="itens")
