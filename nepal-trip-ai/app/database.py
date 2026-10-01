import sqlite3
from pathlib import Path

from flask import current_app, g


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    travel_interest TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def get_db():
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    del error
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def init_database():
    database = get_db()
    database.executescript(SCHEMA)

    columns = [row[1] for row in database.execute("PRAGMA table_info(users)").fetchall()]
    if "username" not in columns:
        database.execute("ALTER TABLE users ADD COLUMN username TEXT")

    database.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username)")
    database.commit()
