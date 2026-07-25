import httpx
from app.config import get_settings

settings = get_settings()
FLUTTERWAVE_BASE_URL = "https://api.flutterwave.com/v3"


def get_headers(secret_key: str) -> dict:
    return {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }


async def initialize_transaction(
    email: str, amount: float, reference: str, currency: str = "NGN",
    phone_number: str = None, secret_key: str = None,
) -> dict:
    key = secret_key or settings.FLUTTERWAVE_SECRET_KEY
    payload = {
        "tx_ref": reference,
        "amount": str(amount),
        "currency": currency,
        "customer": {
            "email": email,
        },
        "redirect_url": "https://yourdomain.com/payment/callback",
    }
    if phone_number:
        payload["customer"]["phone_number"] = phone_number

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FLUTTERWAVE_BASE_URL}/payments",
            headers=get_headers(key),
            json=payload,
        )
        return response.json()


async def verify_transaction(reference: str, secret_key: str = None) -> dict:
    key = secret_key or settings.FLUTTERWAVE_SECRET_KEY
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FLUTTERWAVE_BASE_URL}/transactions/verify?tx_ref={reference}",
            headers=get_headers(key),
        )
        return response.json()


def verify_webhook_signature(signature: str, payload: bytes, secret: str) -> bool:
    import hashlib
    import hmac
    computed = hmac.new(
        secret.encode("utf-8"), hashlib.sha256(payload).digest(), None
    ).hexdigest()
    return hmac.compare_digest(computed, signature)
