from pathlib import Path

from flask import Flask

from .database import init_app, init_database
from .routes import auth_api, pages


def create_app(test_config=None):
    project_root = Path(__file__).resolve().parent.parent
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev-change-this-secret",
        DATABASE=str(project_root / "instance" / "himalaya.sqlite3"),
        PROJECT_ROOT=project_root,
    )

    if test_config is not None:
        app.config.update(test_config)

    init_app(app)
    app.register_blueprint(pages)
    app.register_blueprint(auth_api, url_prefix="/api")

    with app.app_context():
        init_database()

    return app
