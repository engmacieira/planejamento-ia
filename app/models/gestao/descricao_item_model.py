from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.base_model import DefaultModel  

class DescricaoItem(DefaultModel, Base): 
    __tablename__ = "descricao_item"

    descricao: Mapped[str] = mapped_column(String)