from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    DateTime, 
    ForeignKey, 
    Boolean, 
    Date,
    Float,
    Numeric
)
from sqlalchemy.orm import relationship
from models import Base

class UserClient(Base):
    __tablename__ = "user_client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String(36), ForeignKey("user.id"), nullable=False, index=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    isact = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="user_clients")
    client = relationship("Client", back_populates="client_users")