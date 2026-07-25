import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.invoice import Invoice
from app.models.reminder import Reminder
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceListResponse
from app.api.auth import get_current_user
from app.services.tasks import schedule_reminders_for_invoice

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


def generate_reference() -> str:
    return f"RMPAY-{uuid.uuid4().hex[:12].upper()}"


@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(
    data: InvoiceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    invoice = Invoice(
        user_id=current_user.id,
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        customer_phone=data.customer_phone,
        amount=data.amount,
        currency=data.currency,
        description=data.description,
        due_date=data.due_date,
        payment_gateway=data.payment_gateway,
        reference=generate_reference(),
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    schedule_reminders_for_invoice.delay(str(invoice.id))

    return InvoiceResponse.model_validate(invoice)


@router.get("/", response_model=InvoiceListResponse)
def list_invoices(
    status_filter: str = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Invoice).filter(Invoice.user_id == current_user.id)

    if status_filter:
        query = query.filter(Invoice.status == status_filter)

    total = query.count()
    invoices = (
        query.order_by(Invoice.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return InvoiceListResponse(
        invoices=[InvoiceResponse.model_validate(inv) for inv in invoices],
        total=total,
    )


@router.get("/stats")
def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    base_query = db.query(Invoice).filter(Invoice.user_id == current_user.id)

    total = base_query.count()
    paid = base_query.filter(Invoice.status == "paid").count()
    pending = base_query.filter(Invoice.status == "pending").count()
    overdue = base_query.filter(Invoice.status == "overdue").count()

    total_revenue = (
        db.query(func.sum(Invoice.amount))
        .filter(Invoice.user_id == current_user.id, Invoice.status == "paid")
        .scalar()
        or 0
    )

    return {
        "total_invoices": total,
        "paid": paid,
        "pending": pending,
        "overdue": overdue,
        "total_revenue": float(total_revenue),
    }


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.user_id == current_user.id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return InvoiceResponse.model_validate(invoice)


@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: str,
    data: InvoiceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.user_id == current_user.id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(invoice, field, value)

    db.commit()
    db.refresh(invoice)
    return InvoiceResponse.model_validate(invoice)


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.user_id == current_user.id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(invoice)
    db.commit()
