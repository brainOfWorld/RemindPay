from pydantic import BaseModel
from typing import Optional, Any


class PaystackWebhookPayload(BaseModel):
    event: str
    data: dict[str, Any]


class FlutterwaveWebhookPayload(BaseModel):
    event: str
    data: dict[str, Any]


class WebhookResponse(BaseModel):
    status: str
    message: str
