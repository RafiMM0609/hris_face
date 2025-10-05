from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, BigInteger
from sqlalchemy.sql import func
from models import Base

class OutletWilayah(Base):
    __tablename__ = "outlet_wilayah"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    id_wilayah = Column(Integer, ForeignKey("wilayah.id"), nullable=False)
    id_outlet = Column(Integer, ForeignKey("client_outlet.id"), nullable=False)
    isact = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
