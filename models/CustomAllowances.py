from sqlalchemy import (
    Column,
    Numeric, 
    String, 
    Integer, 
    DateTime, 
    ForeignKey, 
    Boolean, 
    DECIMAL, 
    Date,
    Float
)
from sqlalchemy.orm import relationship
from models import Base

class CustomAllowances(Base):
    __tablename__ = "custom_allowance"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    client_id = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=True)
    type_tad = Column(String, nullable=True, index=True)
    amount = Column(Numeric(15, 5), nullable=True)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    isact = Column(Boolean, default=True)
    is_daily = Column(Boolean, default=False)
    feemn = Column(Boolean, nullable=True, default=False)   
    is_fixed = Column(Boolean, nullable=True, default=False)   

