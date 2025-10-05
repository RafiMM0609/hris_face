from sqlalchemy import Boolean, Column, Integer, String, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models import Base

class HistoryActivityEmp(Base):
    __tablename__ = 'history_activity_emp'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=True)
    leave_id = Column(Integer, ForeignKey('leave_table.id'), nullable=True)
    attendance_id = Column(Integer, ForeignKey('attendance.id'), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    isact = Column(Boolean, default=True)
    emp_id = Column(String(36), nullable=False, index=True)

    leave_history = relationship("LeaveTable", back_populates="history_activity_emp")
    attendance_history = relationship("Attendance", back_populates="history_activity_emp")