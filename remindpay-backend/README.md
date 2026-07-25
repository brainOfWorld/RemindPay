# RemindPay Backend

## Prerequisites
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL (or use Docker)
- Redis (or use Docker)

## Quick Start

### 1. Start infrastructure
```bash
docker-compose up -d
```

### 2. Install Python dependencies
```bash
cd remindpay-backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 3. Configure environment
Edit `.env` with your actual keys:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/remindpay
SECRET_KEY=your-random-secret-key
PAYSTACK_SECRET_KEY=sk_test_xxx
FLUTTERWAVE_SECRET_KEY=FLWSECK-xxx
WHATSAPP_PHONE_NUMBER_ID=your_id
WHATSAPP_ACCESS_TOKEN=your_token
```

### 4. Start the API server
```bash
uvicorn app.main:app --reload --port 8000
```
API docs at: http://localhost:8000/docs

### 5. Start the Celery worker (new terminal)
```bash
cd remindpay-backend
celery -A celery_worker worker --beat --loglevel=info
```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account + JWT |
| POST | `/api/auth/login` | Login + JWT |
| GET | `/api/auth/me` | Get current user |
| PUT | `/api/auth/settings` | Update gateway/WhatsApp keys |

### Invoices
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/invoices/` | Create invoice (auto-schedules reminders) |
| GET | `/api/invoices/` | List invoices (filter by status, pagination) |
| GET | `/api/invoices/stats` | Dashboard stats |
| GET | `/api/invoices/{id}` | Get single invoice |
| PUT | `/api/invoices/{id}` | Update invoice |
| DELETE | `/api/invoices/{id}` | Delete invoice |

### Reminders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reminders/{invoice_id}` | List reminders for invoice |
| POST | `/api/reminders/{invoice_id}/trigger/{stage}` | Manually trigger stage 1/2/3 |
| POST | `/api/reminders/{invoice_id}/cancel-all` | Cancel all scheduled reminders |

### Webhooks (no auth)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/webhooks/paystack` | Paystack payment listener |
| POST | `/api/webhooks/flutterwave` | Flutterwave payment listener |

## Testing with curl

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@business.com","password":"secret123","business_name":"My Shop"}'

# Login (save the token)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@business.com","password":"secret123"}'

# Create invoice (replace TOKEN and dates)
curl -X POST http://localhost:8000/api/invoices/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "08012345678",
    "amount": 50000,
    "due_date": "2026-08-01T10:00:00",
    "payment_gateway": "paystack"
  }'
```
