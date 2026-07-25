# RemindPay

Automated WhatsApp payment reminder system integrated with Paystack & Flutterwave.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Next.js     │────▶│  FastAPI      │────▶│  PostgreSQL   │
│  Frontend    │     │  Backend      │     │  Database     │
│  :3000       │     │  :8000        │     │  :5432        │
└─────────────┘     └──────┬───────┘     └──────────────┘
                           │
                    ┌──────┴───────┐
                    │  Celery       │
                    │  Worker       │────▶ Redis :6379
                    │  (Beat)       │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ WhatsApp  │ │ Paystack  │ │Flutterwave│
        │ Cloud API │ │ Webhooks  │ │ Webhooks  │
        └──────────┘ └──────────┘ └──────────┘
```

## How It Works

1. Business owner registers and saves gateway/WhatsApp API keys
2. Creates an invoice with customer details and due date
3. Celery auto-schedules 3 WhatsApp reminders:
   - **Stage 1**: 2 days before due date
   - **Stage 2**: On due date
   - **Stage 3**: 3 days overdue
4. When customer pays via Paystack/Flutterwave, webhook fires
5. Invoice marked as PAID, all remaining reminders auto-cancelled

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose

### 1. Start databases
```bash
docker-compose up -d
```

### 2. Backend
```bash
cd remindpay-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Celery Worker (new terminal)
```bash
cd remindpay-backend
celery -A celery_worker worker --beat --loglevel=info
```

### 4. Frontend (new terminal)
```bash
cd remindpay-frontend
npm install
npm run dev
```

### 5. Open
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/remindpay
SECRET_KEY=change-me
PAYSTACK_SECRET_KEY=sk_test_xxx
FLUTTERWAVE_SECRET_KEY=FLWSECK-xxx
WHATSAPP_PHONE_NUMBER_ID=xxx
WHATSAPP_ACCESS_TOKEN=xxx
REDIS_URL=redis://localhost:6379/0
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Project Structure
```
RemindPay/
├── docker-compose.yml
├── remindpay-backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry
│   │   ├── config.py         # Env settings
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models/           # DB tables
│   │   ├── schemas/          # Pydantic validation
│   │   ├── api/              # Route endpoints
│   │   └── services/         # WhatsApp, Paystack, Flutterwave, Celery
│   ├── celery_worker.py
│   ├── requirements.txt
│   └── .env
└── remindpay-frontend/
    ├── src/
    │   ├── app/              # Next.js pages
    │   ├── components/       # Reusable UI
    │   └── lib/              # API client
    ├── package.json
    └── tailwind.config.js
```
