from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from models import Base

class UserOutlet(Base):
    __tablename__ = "user_outlet"

    id = Column(Integer, primary_key=True, nullable=False)
    emp_id = Column(String(36), ForeignKey("user.id"), nullable=False, index=True)
    outlet_id = Column(Integer, ForeignKey("client_outlet.id_outlet"), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="user_outlets")
    outlet = relationship("ClientOutlet", back_populates="user_outlets")
