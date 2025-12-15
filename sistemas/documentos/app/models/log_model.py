from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base, DefaultModel

class GenerationLog(Base, DefaultModel):
    __tablename__ = "generation_logs"

    # O que foi gerado?
    generated_filename = Column(String, nullable=False)
    
    # FK 1: Quem gerou?
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="logs")

    # FK 2: Qual modelo foi usado?
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    template = relationship("Template", back_populates="logs")