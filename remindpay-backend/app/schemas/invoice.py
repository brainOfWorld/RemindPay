from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal


class InvoiceCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    amount: Decimal
    currency: str = "NGN"
    description: Optional[str] = None
    due_date: datetime
    payment_gateway: Optional[str] = None  # paystack, flutterwave


class InvoiceUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None


class InvoiceResponse(BaseModel):
    id: UUID
    customer_name: str
    customer_email: str
    customer_phone: Optional[str]
    amount: Decimal
    currency: str
    description: Optional[str]
    reference: Optional[str]
    status: str
    payment_gateway: Optional[str]
    payment_link: Optional[str]
    due_date: datetime
    paid_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InvoiceListResponse(BaseModel):
    invoices: list[InvoiceResponse]
    total: int
