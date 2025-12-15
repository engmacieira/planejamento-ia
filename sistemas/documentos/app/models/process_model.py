from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base, DefaultModel

class Processo(Base, DefaultModel):
    __tablename__ = "processos"

    # Campos baseados na sua planilha CSV
    numero_dfd = Column(String, nullable=False) # Ex: 038/2025
    secretaria = Column(String, nullable=False)
    objeto = Column(Text, nullable=False)       # Text pois pode ser longo
    valor_estimado = Column(String, nullable=False) # String para manter formatação (R$ ...)
    valor_extenso = Column(String, nullable=False)
    
    # Campos técnicos e datas
    dotacao = Column(Text, nullable=True) # Pode ser longa
    artigo = Column(String, nullable=True)
    
    # Datas genéricas (Data1 a Data5) conforme sua base
    data1 = Column(String, nullable=True)
    data2 = Column(String, nullable=True)
    data3 = Column(String, nullable=True)
    data4 = Column(String, nullable=True)
    data5 = Column(String, nullable=True)

    # Relacionamento: Quem é o dono desse processo?
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="processos")