from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models import Base

class UserWilayah(Base):
    __tablename__ = "user_wilayah"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    emp_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    id_wilayah = Column(Integer, ForeignKey("wilayah.id"), nullable=False)
    isact = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())


    user = relationship("User", back_populates="user_wilayahs")
    wilayah = relationship("Wilayah", back_populates="user_wilayahs")
