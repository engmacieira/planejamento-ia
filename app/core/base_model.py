from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

class DefaultModel:
    """
    Mixin class modernizada para SQLAlchemy 2.0:
    - id: Primary Key
    - created_at: Creation timestamp
    - updated_at: Update timestamp
    - is_deleted: Soft delete flag
    """
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), default=datetime.utcnow)
    
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")