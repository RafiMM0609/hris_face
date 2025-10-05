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
from models.MasterCompensation import MasterCompensation

class Compensation(Base):
    __tablename__ = "compensation"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    emp_id = Column(String(36), ForeignKey("user.id"), nullable=False, index=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False, index=True)
    service_name = Column(String(255), nullable=True)
    amount = Column(Float, nullable=True)
    payment_date = Column(Date, nullable=True)
    type = Column(Integer, ForeignKey("master_compensation.id"), nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=None)
    updated_at = Column(DateTime(timezone=True), default=None, onupdate=None)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    isact = Column(Boolean, default=True)
    contract_id = Column(Integer, nullable=True)
    parent = Column(Integer, ForeignKey("parent_compensation.id"), nullable=True)
    status_payment = Column(Boolean, nullable=True)

    # Relations
    user = relationship("User", foreign_keys=[emp_id])
    client = relationship("Client", foreign_keys=[client_id])
    master_compensation = relationship("MasterCompensation", back_populates="compensations", foreign_keys=[type])
    parent_compensation = relationship("ParentCompensation", back_populates="compensations", foreign_keys=[parent])
