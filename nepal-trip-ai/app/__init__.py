import os
from pathlib import Path

from flask import Flask

from .database import init_app, init_database
from .routes import auth_api, pages
from .web_app import planner_pages


def create_app(test_config=None):
    project_root = Path(__file__).resolve().parent.parent
    is_production = os.environ.get("FLASK_ENV", "development").lower() == "production"
    debug_mode = os.environ.get("FLASK_DEBUG", "false" if is_production else "true").lower() in {"1", "true", "yes"}
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev-change-this-secret",
        DATABASE=str(project_root / "instance" / "himalaya.sqlite3"),
        PROJECT_ROOT=project_root,
        RESET_PASSWORD_DEMO_MODE=os.environ.get(
            "RESET_PASSWORD_DEMO_MODE", "false" if is_production else "true"
        ).lower() in {"1", "true", "yes"},
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
    )

    if test_config is not None:
        app.config.update(test_config)

    init_app(app)
    app.register_blueprint(pages)
    app.register_blueprint(auth_api, url_prefix="/api")
    app.register_blueprint(planner_pages, url_prefix="/dashboard")

    with app.app_context():
        init_database()

    return app
