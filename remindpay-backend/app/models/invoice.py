import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(50), nullable=True)

    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="NGN")
    description = Column(Text, nullable=True)
    reference = Column(String(255), unique=True, nullable=True, index=True)

    status = Column(String(20), default="pending", index=True)  # pending, paid, overdue, cancelled
    payment_gateway = Column(String(20), nullable=True)  # paystack, flutterwave
    payment_link = Column(Text, nullable=True)

    due_date = Column(DateTime, nullable=False)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="invoices")
    reminders = relationship("Reminder", back_populates="invoice", cascade="all, delete-orphan")
