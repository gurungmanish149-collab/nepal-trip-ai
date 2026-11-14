import os
import hmac
import secrets
from pathlib import Path

from flask import Flask, abort, jsonify, request, session

from .database import get_db, init_app, init_database
from .routes import auth_api, pages
from .web_app import planner_pages


def create_app(test_config=None):
    project_root = Path(__file__).resolve().parent.parent
    is_production = os.environ.get("FLASK_ENV", "development").lower() == "production"
    debug_mode = os.environ.get("FLASK_DEBUG", "false" if is_production else "true").lower() in {"1", "true", "yes"}
    secret_key = os.environ.get("SECRET_KEY")
    if is_production and not secret_key and test_config is None:
        raise RuntimeError("SECRET_KEY must be configured before starting in production.")
    if is_production and secret_key and len(secret_key) < 32 and test_config is None:
        raise RuntimeError("SECRET_KEY must contain at least 32 characters in production.")
    demo_reset_mode = os.environ.get("RESET_PASSWORD_DEMO_MODE", "false" if is_production else "true").lower() in {
        "1", "true", "yes"
    }
    if is_production and demo_reset_mode and test_config is None:
        raise RuntimeError("RESET_PASSWORD_DEMO_MODE must be disabled in production.")

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=secret_key or secrets.token_urlsafe(32),
        IS_PRODUCTION=is_production,
        DATABASE=os.environ.get("DATABASE", str(project_root / "instance" / "himalaya.sqlite3")),
        PROJECT_ROOT=project_root,
        PUBLIC_BASE_URL=os.environ.get("PUBLIC_BASE_URL", "").rstrip("/"),
        RESET_PASSWORD_DEMO_MODE=demo_reset_mode,
        SMTP_HOST=os.environ.get("SMTP_HOST"),
        SMTP_PORT=os.environ.get("SMTP_PORT", "587"),
        SMTP_USERNAME=os.environ.get("SMTP_USERNAME"),
        SMTP_PASSWORD=os.environ.get("SMTP_PASSWORD"),
        SMTP_FROM=os.environ.get("SMTP_FROM"),
        SMTP_USE_TLS=os.environ.get("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes"},
        DEBUG=debug_mode,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=is_production,
        MAX_CONTENT_LENGTH=64 * 1024,
    )

    if test_config is not None:
        app.config.update(test_config)

    init_app(app)

    @app.before_request
    def protect_authenticated_mutations():
        if not session.get("csrf_token"):
            session["csrf_token"] = secrets.token_urlsafe(32)

        user_id = session.get("user_id")
        if user_id is not None:
            row = get_db().execute(
                "SELECT auth_version FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            if row is None or session.get("auth_version") != row["auth_version"]:
                session.clear()
                session["csrf_token"] = secrets.token_urlsafe(32)

        protected_endpoints = {
            "auth_api.signup",
            "auth_api.signin",
            "auth_api.wishlist",
            "auth_api.signout",
            "auth_api.trip_inquiries",
            "planner_pages.planner_signout",
        }
        if request.method in {"POST", "PUT", "PATCH", "DELETE"} and request.endpoint in protected_endpoints:
            expected = session.get("csrf_token", "")
            supplied = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token", "")
            if not expected or not supplied or not hmac.compare_digest(expected, supplied):
                if request.path.startswith("/api/"):
                    return jsonify({"error": "Your session token is missing or expired. Refresh and try again."}), 400
                abort(400)

    @app.context_processor
    def inject_security_context():
        return {"csrf_token": session.get("csrf_token", "")}

    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        if request.path.startswith("/api/") or request.path in {
            "/signin.html",
            "/signup.html",
            "/forgot-password.html",
            "/reset-password.html",
        }:
            response.headers["Cache-Control"] = "no-store"
        return response

    app.register_blueprint(pages)
    app.register_blueprint(auth_api, url_prefix="/api")
    app.register_blueprint(planner_pages, url_prefix="/dashboard")

    with app.app_context():
        init_database()

    return app
