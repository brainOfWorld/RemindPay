import httpx
from app.config import get_settings

settings = get_settings()
PAYSTACK_BASE_URL = "https://api.paystack.co"


def get_headers(secret_key: str) -> dict:
    return {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }


async def initialize_transaction(
    email: str, amount: float, reference: str, currency: str = "NGN",
    metadata: dict = None, secret_key: str = None,
) -> dict:
    key = secret_key or settings.PAYSTACK_SECRET_KEY
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYSTACK_BASE_URL}/transaction/initialize",
            headers=get_headers(key),
            json={
                "email": email,
                "amount": int(amount * 100),  # Paystack uses kobo
                "reference": reference,
                "currency": currency,
                "metadata": metadata or {},
            },
        )
        return response.json()


async def verify_transaction(reference: str, secret_key: str = None) -> dict:
    key = secret_key or settings.PAYSTACK_SECRET_KEY
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
            headers=get_headers(key),
        )
        return response.json()


def verify_webhook_signature(signature: str, payload: bytes, secret: str) -> bool:
    import hashlib
    import hmac
    computed = hmac.new(
        secret.encode("utf-8"), payload, hashlib.sha512
    ).hexdigest()
    return hmac.compare_digest(computed, signature)
