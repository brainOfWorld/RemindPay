from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.invoice import Invoice
from app.models.reminder import Reminder
from app.api.auth import get_current_user
from app.services.whatsapp import send_reminder

router = APIRouter(prefix="/api/reminders", tags=["reminders"])


@router.get("/{invoice_id}")
def list_reminders(
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

    reminders = (
        db.query(Reminder)
        .filter(Reminder.invoice_id == invoice_id)
        .order_by(Reminder.stage)
        .all()
    )

    return [
        {
            "id": str(r.id),
            "stage": r.stage,
            "scheduled_at": r.scheduled_at.isoformat() if r.scheduled_at else None,
            "sent_at": r.sent_at.isoformat() if r.sent_at else None,
            "status": r.status,
            "message_content": r.message_content,
            "whatsapp_message_id": r.whatsapp_message_id,
            "error_message": r.error_message,
            "created_at": r.created_at.isoformat(),
        }
        for r in reminders
    ]


@router.post("/{invoice_id}/trigger/{stage}")
async def trigger_reminder(
    invoice_id: str,
    stage: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if stage not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Stage must be 1, 2, or 3")

    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.user_id == current_user.id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.status == "paid":
        raise HTTPException(status_code=400, detail="Invoice is already paid")

    existing = (
        db.query(Reminder)
        .filter(Reminder.invoice_id == invoice_id, Reminder.stage == stage)
        .first()
    )

    if existing and existing.status == "sent":
        raise HTTPException(status_code=400, detail="Reminder already sent for this stage")

    if existing:
        reminder = existing
    else:
        reminder = Reminder(
            invoice_id=invoice.id,
            stage=stage,
            scheduled_at=datetime.utcnow(),
        )
        db.add(reminder)
        db.commit()
        db.refresh(reminder)

    success = await send_reminder(reminder, invoice, db)

    if success:
        return {"status": "sent", "reminder_id": str(reminder.id)}
    else:
        raise HTTPException(status_code=500, detail=f"Failed to send: {reminder.error_message}")


@router.post("/{invoice_id}/cancel-all")
def cancel_all_reminders(
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

    cancelled = (
        db.query(Reminder)
        .filter(
            Reminder.invoice_id == invoice_id,
            Reminder.status == "scheduled",
        )
        .update({"status": "cancelled"})
    )
    db.commit()

    return {"cancelled": cancelled}
