from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr

class DefaultModel:
    """
    Mixin class that provides default columns for all models:
    - id: Primary Key
    - created_at: Creation timestamp
    - updated_at: Update timestamp
    - is_deleted: Soft delete flag
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft Delete: Em vez de apagar, marcamos como True
    is_deleted = Column(Boolean, default=False)
