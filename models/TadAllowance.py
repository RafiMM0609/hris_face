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

class TadAllowance(Base):
    __tablename__ = "tad_allowance"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    client_id = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    type_tad = Column(String(255), nullable=False, index=True)
    emp_id = Column(String(36), nullable=False)
    amount = Column(Numeric(15, 5), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    isact = Column(Boolean, default=True)
    is_daily = Column(Boolean, nullable=False, default=False)
    feemn = Column(Boolean, nullable=True, default=None)
    is_fixed = Column(Boolean, nullable=True, default=False)
