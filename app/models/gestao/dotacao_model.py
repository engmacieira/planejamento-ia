from decimal import Decimal
from sqlalchemy import String, Integer, Boolean, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Dotacao(Base):
    __tablename__ = "dotacao"
    
    __table_args__ = (
        CheckConstraint("exercicio IS NOT NULL", name="check_exercicio_not_null"), # Implicit in SQL NOT NULL
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    exercicio: Mapped[int] = mapped_column(Integer)
    codigo_dotacao: Mapped[str] = mapped_column(String(100))
    
    numero_ficha: Mapped[int | None] = mapped_column(Integer, nullable=True)
    descricao: Mapped[str | None] = mapped_column(String, nullable=True) # Text in SQL maps to String
    
    saldo_inicial: Mapped[Decimal | None] = mapped_column(Numeric(15, 2), nullable=True)
    
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
