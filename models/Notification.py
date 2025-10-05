import uuid
from sqlalchemy import (
    Column,
    DateTime,
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


class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(255), nullable=True)
    is_mobile = Column(Boolean, default=False)
    emp_id = Column(String(36), ForeignKey("user.id"), nullable=True, index=True)
    client_id = Column(Integer, nullable=True)
    role_id = Column(Integer, nullable=True)
    id_contract = Column(Integer, ForeignKey("contract.id"), nullable=True)
    id_leave = Column(Integer, ForeignKey("leave_table.id"),nullable=True)
    id_payslip = Column(Integer, ForeignKey("payroll.id"),nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_onupdate=func.now())
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    is_read = Column(Boolean, default=False)
    isact = Column(Boolean, default=True)
    type = Column(String(100), nullable=True)
    title = Column(String(255), nullable=True)
    path = Column(String(255), nullable=True)

    # Relationship
    user = relationship("User", back_populates="notifications")
    contract = relationship("Contract", back_populates="notifications", foreign_keys=[id_contract])
    leave = relationship("LeaveTable", back_populates="notifications", foreign_keys=[id_leave])
    payslip = relationship("Payroll", back_populates="notifications", foreign_keys=[id_payslip])


