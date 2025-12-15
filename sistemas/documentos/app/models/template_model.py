from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base, DefaultModel

class Template(Base, DefaultModel):
    __tablename__ = "templates"

    # Campos do Arquivo
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False) # Caminho onde salvamos o .docx
    description = Column(String, nullable=True)

    # --- O RELACIONAMENTO (Foreign Key) ---
    # Aqui dizemos: "Esta coluna guarda o ID da tabela 'users'"
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # --- NAVEGAÇÃO (ORM) ---
    # Aqui dizemos ao Python: "Quando eu acessar .owner, traga o objeto User completo"
    # O back_populates tem que bater com o nome que colocamos lá no User ("templates")
    owner = relationship("User", back_populates="templates")

    # Preparando o terreno para o próximo model (Logs)
    logs = relationship("GenerationLog", back_populates="template")