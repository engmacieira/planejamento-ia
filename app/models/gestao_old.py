from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Numeric, UniqueConstraint, CheckConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255))
    cpf_cnpj = Column(String(18), unique=True, nullable=False)
    email = Column(String(255))
    telefone = Column(String(20))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    contratos = relationship("Contrato", back_populates="fornecedor")


class InstrumentoContratual(Base):
    __tablename__ = "instrumentos_contratuais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    contratos = relationship("Contrato", back_populates="instrumento")


class AgenteResponsavel(Base):
    __tablename__ = "agentes_responsaveis"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    email = Column(String(255))
    telefone = Column(String(20))
    cargo = Column(String(100))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now())


class LocalEntrega(Base):
    __tablename__ = "locais_entrega"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), unique=True, nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100))
    bairro = Column(String(100), nullable=False)
    cep = Column(String(10))
    telefone_contato = Column(String(20))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())


class Dotacao(Base):
    __tablename__ = "dotacao"

    id = Column(Integer, primary_key=True, index=True)
    exercicio = Column(Integer, nullable=False)
    codigo_dotacao = Column(String(100), nullable=False)
    numero_ficha = Column(Integer)
    descricao = Column(Text)
    saldo_inicial = Column(Numeric(15, 2))
    ativo = Column(Boolean, default=True)
    
    __table_args__ = (
        UniqueConstraint('exercicio', 'codigo_dotacao', name='uk_dotacao_exercicio_codigo'),
    )


class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    numero_contrato = Column(Integer, nullable=False)
    ano_contrato = Column(Integer, nullable=False)
    
    id_processo_licitatorio = Column(Integer, ForeignKey("processos_licitatorios.id"), nullable=False)
    id_numero_modalidade = Column(Integer, ForeignKey("numeros_modalidade.id"), nullable=False)
    id_fornecedor = Column(Integer, ForeignKey("fornecedores.id"), nullable=False)
    id_instrumento_contratual = Column(Integer, ForeignKey("instrumentos_contratuais.id"))
    
    data_assinatura = Column(Date, nullable=False)
    data_inicio_vigencia = Column(Date, nullable=False)
    data_fim_vigencia = Column(Date, nullable=False)
    
    valor_total = Column(Numeric(15, 2), default=0)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('numero_contrato', 'ano_contrato', name='uk_contrato_full'),
        CheckConstraint('data_fim_vigencia >= data_inicio_vigencia', name='check_vigencia'),
    )

    processo_licitatorio = relationship("ProcessoLicitatorio", back_populates="contratos")
    numero_modalidade = relationship("NumeroModalidade", backref="contratos")
    fornecedor = relationship("Fornecedor", back_populates="contratos")
    instrumento = relationship("InstrumentoContratual", back_populates="contratos")
    itens = relationship("ItemContrato", back_populates="contrato", cascade="all, delete-orphan")
    anexos = relationship("Anexo", back_populates="contrato", cascade="all, delete-orphan")


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

    contrato = relationship("Contrato", back_populates="itens")
    item_dfd = relationship("ItemDFD")


class AOCS(Base):
    __tablename__ = "aocs"

    id = Column(Integer, primary_key=True, index=True)
    numero_aocs = Column(String(100), unique=True, nullable=False)
    ano_aocs = Column(Integer, nullable=False)
    numero_pedido_externo = Column(String(50))
    data_emissao = Column(Date, nullable=False, server_default=func.current_date())
    
    id_unidade_requisitante = Column(Integer, ForeignKey("unidades_requisitantes.id"), nullable=False)
    id_solicitante = Column(Integer, ForeignKey("agentes_responsaveis.id"))
    id_agente_responsavel = Column(Integer, ForeignKey("agentes_responsaveis.id"))
    
    id_local_entrega = Column(Integer, ForeignKey("locais_entrega.id"))
    id_dotacao = Column(Integer, ForeignKey("dotacao.id"))
    empenho = Column(String(50))
    
    status = Column(String(30), default='Emitida')
    justificativa = Column(Text)
    
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    unidade_requisitante = relationship("UnidadeRequisitante")
    solicitante = relationship("AgenteResponsavel", foreign_keys=[id_solicitante])
    agente_responsavel = relationship("AgenteResponsavel", foreign_keys=[id_agente_responsavel])
    local_entrega = relationship("LocalEntrega")
    dotacao = relationship("Dotacao")
    anexos = relationship("Anexo", back_populates="aocs", cascade="all, delete-orphan")
