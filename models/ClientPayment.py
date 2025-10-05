import uuid
from sqlalchemy import TIMESTAMP
from sqlalchemy import (
    Column,
    Numeric, 
    String, 
    Integer, 
    Date,
    ForeignKey, 
    Boolean, 
    Float,
    func,
)
from sqlalchemy.orm import relationship
from models import Base
from models.StatusPayment import StatusPayment


class ClientPayment(Base):
    __tablename__ = "client_payment"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=True, index=True)
    amount = Column(Numeric(15, 5), nullable=True)
    date = Column(Date, nullable=True)
    status = Column(Integer, ForeignKey("master_status_payment.id"), nullable=True)
    evidence = Column(String(255), nullable=True)
    isact = Column(Boolean, default=True)
    evidence_leave = Column(String(255), nullable=True)
    billing_group_id= Column(String(36), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Many to One
    clients = relationship("Client", back_populates="client_payments", foreign_keys=[client_id])
    status_payment = relationship("StatusPayment", back_populates="payments", foreign_keys=[status])
