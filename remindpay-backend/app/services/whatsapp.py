import httpx
from datetime import datetime
from app.config import get_settings

settings = get_settings()


def build_payment_link(invoice) -> str:
    if invoice.payment_link:
        return invoice.payment_link
    return "https://yourdomain.com/pay"


def build_stage_1_message(invoice, payment_link: str) -> str:
    return (
        f"Hello {invoice.customer_name},\n\n"
        f"This is a friendly reminder that your payment of {invoice.currency} {invoice.amount} "
        f"is due on {invoice.due_date.strftime('%d %B %Y')}.\n\n"
        f"Description: {invoice.description or 'N/A'}\n\n"
        f"Click below to pay now:\n{payment_link}\n\n"
        f"Thank you!"
    )


def build_stage_2_message(invoice, payment_link: str) -> str:
    return (
        f"Hi {invoice.customer_name},\n\n"
        f"Your payment of {invoice.currency} {invoice.amount} is due TODAY.\n\n"
        f"Please make payment to avoid any delays.\n\n"
        f"Pay here: {payment_link}\n\n"
        f"Thank you!"
    )


def build_stage_3_message(invoice, payment_link: str) -> str:
    return (
        f"Dear {invoice.customer_name},\n\n"
        f"Your payment of {invoice.currency} {invoice.amount} was due on "
        f"{invoice.due_date.strftime('%d %B %Y')} and is now OVERDUE.\n\n"
        f"Please settle this payment immediately to avoid further action.\n\n"
        f"Pay now: {payment_link}\n\n"
        f"Thank you."
    )


def build_message(stage: int, invoice, payment_link: str) -> str:
    builders = {1: build_stage_1_message, 2: build_stage_2_message, 3: build_stage_3_message}
    return builders[stage](invoice, payment_link)


async def send_text_message(
    to_phone: str, message: str, phone_number_id: str = None, access_token: str = None
) -> dict:
    pid = phone_number_id or settings.WHATSAPP_PHONE_NUMBER_ID
    token = access_token or settings.WHATSAPP_ACCESS_TOKEN

    formatted_phone = to_phone.replace("+", "").replace(" ", "").replace("-", "")
    if not formatted_phone.startswith("234"):
        formatted_phone = "234" + formatted_phone.lstrip("0")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.WHATSAPP_API_URL}/{pid}/messages",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "messaging_product": "whatsapp",
                "to": formatted_phone,
                "type": "text",
                "text": {"body": message},
            },
        )
        return response.json()


async def send_reminder(reminder, invoice, db) -> bool:
    if not invoice.customer_phone:
        reminder.status = "failed"
        reminder.error_message = "No customer phone number"
        db.commit()
        return False

    payment_link = build_payment_link(invoice)
    message_content = build_message(reminder.stage, invoice, payment_link)
    reminder.message_content = message_content

    try:
        user = invoice.user
        result = await send_text_message(
            to_phone=invoice.customer_phone,
            message=message_content,
            phone_number_id=user.whatsapp_phone_number_id,
            access_token=user.whatsapp_access_token,
        )

        if result.get("messages"):
            reminder.whatsapp_message_id = result["messages"][0].get("id")
            reminder.status = "sent"
            reminder.sent_at = datetime.utcnow()
        else:
            reminder.status = "failed"
            reminder.error_message = str(result)
    except Exception as e:
        reminder.status = "failed"
        reminder.error_message = str(e)

    db.commit()
    return reminder.status == "sent"
