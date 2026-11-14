# NepalTrip AI

Himalaya is a Flask travel-discovery application for planning Nepal journeys. It includes destination discovery, travel estimates, account authentication, a persistent wishlist, and password recovery.

## Run the web application

```bash
python3 app/web_app.py
```

Then visit `http://127.0.0.1:5000/index.html`.

The command-line itinerary planner remains available:

```bash
python3 -m app.main
```

## Password recovery

Local development uses a safe demo mode by default. After requesting a reset, the reset page shows a one-hour demo link instead of sending an email.

For real email delivery, set these environment variables and disable demo mode:

```bash
export FLASK_ENV=production
export SECRET_KEY=replace-with-a-long-random-value
export RESET_PASSWORD_DEMO_MODE=false
export SMTP_HOST=smtp.example.com
export SMTP_PORT=587
export SMTP_USERNAME=your-smtp-user
export SMTP_PASSWORD=your-smtp-password
export SMTP_FROM=no-reply@example.com
```

In production, no reset link is exposed in the browser. If SMTP is not configured, the API clearly reports that recovery email is unavailable rather than pretending an email was sent.

## Test

```bash
pytest -q
```
