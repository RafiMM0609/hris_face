from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    DateTime, 
    ForeignKey, 
    Boolean, 
    Date,
    Float,
    Numeric,
    Text
)
from sqlalchemy.orm import relationship
from models import Base

class MasterCompensation(Base):
    __tablename__ = "master_compensation"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    isact = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=None)
    update_at = Column(DateTime(timezone=True), default=None, onupdate=None)
    style = Column(Text, nullable=True)

    # Relationship
    compensations = relationship("Compensation", back_populates="master_compensation")
    compensations_parent = relationship("ParentCompensation", back_populates="master_compensation")