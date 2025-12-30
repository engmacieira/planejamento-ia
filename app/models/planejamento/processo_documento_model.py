from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.core.user_model import User

class ProcessoDocumento(Base):
    __tablename__ = "processos" # Table name from legacy process_model.py

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    numero_dfd: Mapped[str] = mapped_column(String)
    secretaria: Mapped[str] = mapped_column(String)
    objeto: Mapped[str] = mapped_column(Text)
    valor_estimado: Mapped[str] = mapped_column(String)
    valor_extenso: Mapped[str] = mapped_column(String)
    
    dotacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    artigo: Mapped[str | None] = mapped_column(String, nullable=True)
    
    data1: Mapped[str | None] = mapped_column(String, nullable=True)
    data2: Mapped[str | None] = mapped_column(String, nullable=True)
    data3: Mapped[str | None] = mapped_column(String, nullable=True)
    data4: Mapped[str | None] = mapped_column(String, nullable=True)
    data5: Mapped[str | None] = mapped_column(String, nullable=True)
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    owner: Mapped["User"] = relationship("User", back_populates="processos")
