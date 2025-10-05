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
    Time
)
from sqlalchemy.orm import relationship
from models import Base

class MasterShift(Base):
    __tablename__ = 'master_shift'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_start = Column("timestart",Time, nullable=False)
    time_end = Column("timeend",Time, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    isact = Column(Boolean, nullable=True, default=False)
    
    # Relationships
    attendances = relationship("Attendance", back_populates="master_shift")