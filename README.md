# BATMAN TECH Billing

Hotspot billing for BATMAN TECH. The customer portal, admin dashboard, billing logic, and network integration are separated so each can grow independently.

## Layout

- `app/` FastAPI API, models, routers, and services
- `portal/` customer payment pages
- `admin/` operator dashboard
- `migrations/` Alembic schema history
- `tests/` API smoke tests

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

On Ubuntu:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`DATABASE_URL` in `.env.example` targets PostgreSQL. Local development can use SQLite until Postgres is available.

## Run

```bash
uvicorn app.main:app --reload
```

- http://127.0.0.1:8000/ — API status
- http://127.0.0.1:8000/health — health check
- http://127.0.0.1:8000/docs — interactive docs
- http://127.0.0.1:8000/portal — customer portal
- http://127.0.0.1:8000/admin-ui — admin pages

The API is the billing backend. M-Pesa Daraja and live MikroTik access still need credentials; package purchase currently records a payment and a timed subscription.

## Packages (KES)

Durations are stored in seconds.

| Package | Price | Duration (seconds) |
| --- | --- | --- |
| 1 hour | 10 | 3600 |
| 3 hours | 20 | 10800 |
| 12 hours | 25 | 43200 |
| 24 hours | 35 | 86400 |
| 3 days | 110 | 259200 |
| 1 week | 230 | 604800 |

Expiry is `started_at + duration_seconds`. `POST /admin/subscriptions/expire` marks due subscriptions expired and queues RADIUS disconnect.
