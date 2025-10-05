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
from models.Compensation import Compensation    

# Model for parent_compensation table
class ParentCompensation(Base):
    __tablename__ = "parent_compensation"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    service_name = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    type = Column(Integer, ForeignKey("master_compensation.id"), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    isact = Column(Boolean, default=True)
    description = Column(String(255), nullable=True)
    created_by = Column(String(36), nullable=True)
    status_payment = Column(Boolean, nullable=True)

    # Relations
    compensations = relationship(
        "Compensation",
        back_populates="parent_compensation",
        foreign_keys="Compensation.parent",
        primaryjoin="and_(ParentCompensation.id==Compensation.parent, Compensation.isact==True)"
    )
    client = relationship("Client", foreign_keys=[client_id])
    master_compensation = relationship("MasterCompensation", back_populates="compensations_parent", foreign_keys=[type])


