from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class DescricaoItem(Base):
    __tablename__ = "descricao_item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    descricao: Mapped[str] = mapped_column(String)
