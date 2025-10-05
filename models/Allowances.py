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


class Allowances(Base):
    __tablename__ = "allowances"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    client_id = Column(Integer,ForeignKey("client.id"), nullable=False, index=True)
    name = Column(String, nullable=True)
    amount = Column(Numeric(15, 5), nullable=True)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    isact = Column(Boolean, default=True)
    is_daily = Column(Boolean, default=False)
    feemn = Column(Boolean, nullable=True, default=False)
    is_fixed = Column(Boolean, nullable=True, default=False)
    
    # Relation
    client = relationship("Client", back_populates="allowances")