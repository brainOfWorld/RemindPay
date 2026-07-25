from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import get_settings
from app.api.auth import router as auth_router
from app.api.invoices import router as invoices_router
from app.api.webhooks import router as webhooks_router
from app.api.reminders import router as reminders_router

settings = get_settings()

app = FastAPI(title="RemindPay API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://remind-pay.vercel.app",
        "https://remind-pay-hnvi.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(invoices_router)
app.include_router(webhooks_router)
app.include_router(reminders_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "RemindPay API is running"}
