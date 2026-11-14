# NepalTrip AI

Himalaya is a Flask travel-discovery and itinerary-planning app for Nepal. It includes destination discovery, travel estimates, account authentication, a persistent wishlist, password recovery, and non-binding trip inquiries.

## Run locally

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 -m flask --app app:create_app run --host 127.0.0.1 --port 5000
```

Open `http://127.0.0.1:5000/`. The default SQLite database is created at `instance/himalaya.sqlite3`; set `DATABASE` to use another path.

## Password recovery and production configuration

Local development uses a safe demo mode by default. After requesting a reset, the reset page shows a one-hour, single-use demo link. It is not enabled by default in production.

For production, set a unique, long random `SECRET_KEY`, the public HTTPS origin, and SMTP settings before starting the app:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=false
export SECRET_KEY='a-long-random-secret-from-your-secret-manager'
export PUBLIC_BASE_URL='https://travel.example.com'
export RESET_PASSWORD_DEMO_MODE=false
export SMTP_HOST='smtp.example.com'
export SMTP_PORT=587
export SMTP_USERNAME='your-smtp-user'
export SMTP_PASSWORD='your-smtp-password'
export SMTP_FROM='no-reply@example.com'
```

Do not commit production secrets. Production startup fails when `SECRET_KEY` is missing, and password recovery reports that delivery is unavailable when SMTP or the public URL is not configured. Configure HTTPS at the serving proxy so secure session cookies can be used. The application adds security response headers, protects signed-in state changes with CSRF tokens, invalidates existing sessions after a password reset, and applies SQLite-backed request limits to sign-in, signup, password recovery, and trip inquiries.

Trip inquiries are stored with a pending status and are not confirmed bookings; the app does not process payments or connect to a travel provider.

## Tests

```bash
python3 -m pytest -q
```
