from sqlalchemy import Column, Integer, Numeric, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class TypeTad(Base):
    __tablename__ = "type_tad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20))
    id_client = Column(Integer, ForeignKey("client.id"))
    type_tad = Column(String(255))
    type_employee = Column(String(255))
    positional_allowance = Column(Numeric(15, 5))
    created_at = Column(DateTime, default=None)
    updated_at = Column(DateTime, nullable=True)
    isact = Column(Boolean, default=True)

    client = relationship("Client", back_populates="type_tads")
    users = relationship("User", back_populates="type_tad_rel", foreign_keys="User.type_tad")
