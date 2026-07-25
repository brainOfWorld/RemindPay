from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.invoice import Invoice
from app.models.reminder import Reminder
from app.config import get_settings
from app.schemas.webhook import WebhookResponse
from app.services import paystack, flutterwave

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])
settings = get_settings()


def mark_invoice_paid(invoice: Invoice, db: Session):
    invoice.status = "paid"
    invoice.paid_at = datetime.utcnow()
    db.commit()

    db.query(Reminder).filter(
        Reminder.invoice_id == invoice.id,
        Reminder.status == "scheduled",
    ).update({"status": "cancelled"})
    db.commit()


@router.post("/paystack")
async def paystack_webhook(request: Request):
    body = await request.body()
    payload = await request.json()

    event = payload.get("event")
    data = payload.get("data", {})
    reference = data.get("reference")

    if not reference:
        raise HTTPException(status_code=400, detail="Missing reference")

    db = SessionLocal()
    try:
        invoice = db.query(Invoice).filter(Invoice.reference == reference).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        if event == "charge.success":
            verification = await paystack.verify_transaction(
                reference, secret_key=invoice.user.paystack_secret_key
            )
            if verification.get("data", {}).get("status") == "success":
                mark_invoice_paid(invoice, db)
                return WebhookResponse(status="success", message="Invoice marked as paid")

        return WebhookResponse(status="ignored", message="Event not handled")
    finally:
        db.close()


@router.post("/flutterwave")
async def flutterwave_webhook(request: Request):
    body = await request.body()
    payload = await request.json()

    event = payload.get("event")
    data = payload.get("data", {})
    reference = data.get("tx_ref")

    if not reference:
        raise HTTPException(status_code=400, detail="Missing tx_ref")

    db = SessionLocal()
    try:
        invoice = db.query(Invoice).filter(Invoice.reference == reference).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        if event == "charge.completed":
            verification = await flutterwave.verify_transaction(
                reference, secret_key=invoice.user.flutterwave_secret_key
            )
            if verification.get("data", {}).get("status") == "successful":
                mark_invoice_paid(invoice, db)
                return WebhookResponse(status="success", message="Invoice marked as paid")

        return WebhookResponse(status="ignored", message="Event not handled")
    finally:
        db.close()
