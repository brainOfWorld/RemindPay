from datetime import datetime, timedelta
from celery import shared_task
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.invoice import Invoice
from app.models.reminder import Reminder


@shared_task(name="app.services.worker.schedule_reminders_for_invoice")
def schedule_reminders_for_invoice(invoice_id: str):
    db = SessionLocal()
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice or invoice.status != "pending":
            return {"status": "skipped", "reason": "invoice not found or not pending"}

        due_date = invoice.due_date
        stages = [
            (1, due_date - timedelta(days=2)),
            (2, due_date),
            (3, due_date + timedelta(days=3)),
        ]

        created = 0
        for stage, scheduled_at in stages:
            if scheduled_at < datetime.utcnow():
                continue

            existing = (
                db.query(Reminder)
                .filter(Reminder.invoice_id == invoice_id, Reminder.stage ==stage)
                .first()
            )
            if not existing:
                reminder = Reminder(
                    invoice_id=invoice.id,
                    stage=stage,
                    scheduled_at=scheduled_at,
                )
                db.add(reminder)
                created += 1

        db.commit()
        return {"status": "scheduled", "created": created}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@shared_task(name="app.services.worker.check_and_send_reminders")
def check_and_send_reminders():
    from app.services.whatsapp import send_reminder

    db = SessionLocal()
    try:
        now = datetime.utcnow()
        due_reminders = (
            db.query(Reminder)
            .filter(
                Reminder.status == "scheduled",
                Reminder.scheduled_at <= now,
            )
            .all()
        )

        results = []
        for reminder in due_reminders:
            invoice = db.query(Invoice).filter(Invoice.id == reminder.invoice_id).first()
            if not invoice:
                reminder.status = "failed"
                reminder.error_message = "Invoice not found"
                db.commit()
                continue

            if invoice.status == "paid":
                reminder.status = "cancelled"
                db.commit()
                continue

            import asyncio
            loop = asyncio.new_event_loop()
            success = loop.run_until_complete(send_reminder(reminder, invoice, db))
            loop.close()

            results.append({"reminder_id": str(reminder.id), "sent": success})

        return {"checked": len(due_reminders), "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@shared_task(name="app.services.worker.check_overdue_invoices")
def check_overdue_invoices():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        updated = (
            db.query(Invoice)
            .filter(
                Invoice.status == "pending",
                Invoice.due_date < now,
            )
            .update({"status": "overdue"})
        )
        db.commit()
        return {"overdue_updated": updated}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
