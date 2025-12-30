from decimal import Decimal
from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class VSaldoItemContrato(Base):
    """
    Representa a View de Saldos de Itens de Contrato.
    Somente Leitura (ReadOnly).
    """
    __tablename__ = "v_saldo_itens_contrato"
    
    __table_args__ = {"info": {"is_view": True}} 

    id_item_contrato: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    id_contrato: Mapped[int] = mapped_column(Integer)
    nome_item: Mapped[str] = mapped_column(String)
    
    quantidade_contratada: Mapped[Decimal] = mapped_column(Numeric(15, 3))
    total_consumido: Mapped[Decimal] = mapped_column(Numeric(15, 3))
    saldo_disponivel: Mapped[Decimal] = mapped_column(Numeric(15, 3))