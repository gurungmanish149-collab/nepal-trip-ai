import hashlib
import secrets
import time
from dataclasses import dataclass

from werkzeug.security import check_password_hash, generate_password_hash

from .database import get_db


@dataclass
class User:
    id: int
    full_name: str
    username: str
    email: str
    travel_interest: str


def create_user(full_name, username, email, password, travel_interest):
    database = get_db()
    cursor = database.execute(
        """
        INSERT INTO users (full_name, username, email, password_hash, travel_interest)
        VALUES (?, ?, ?, ?, ?)
        """,
        (full_name, username, email, generate_password_hash(password), travel_interest),
    )
    database.commit()
    return User(cursor.lastrowid, full_name, username, email, travel_interest)


def find_user_by_email(email):
    return get_db().execute(
        "SELECT id, full_name, username, email, password_hash, travel_interest FROM users WHERE email = ?",
        (email,),
    ).fetchone()


def find_user_by_username(username):
    return get_db().execute(
        "SELECT id, full_name, username, email, password_hash, travel_interest FROM users WHERE username = ?",
        (username,),
    ).fetchone()


def authenticate_user(email, password):
    user = find_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        return None
    return User(user["id"], user["full_name"], user["username"], user["email"], user["travel_interest"])


def create_password_reset_token(user_id, lifetime_seconds=3600):
    """Create a one-time opaque token and store only its digest."""
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    database = get_db()
    database.execute("DELETE FROM password_reset_tokens WHERE user_id = ?", (user_id,))
    database.execute(
        """
        INSERT INTO password_reset_tokens (user_id, token_hash, expires_at)
        VALUES (?, ?, ?)
        """,
        (user_id, token_hash, int(time.time()) + lifetime_seconds),
    )
    database.commit()
    return token


def reset_password_with_token(token, new_password):
    if not token:
        return False

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = int(time.time())
    database = get_db()
    reset_record = database.execute(
        """
        SELECT id, user_id FROM password_reset_tokens
        WHERE token_hash = ? AND used_at IS NULL AND expires_at >= ?
        """,
        (token_hash, now),
    ).fetchone()
    if reset_record is None:
        return False

    database.execute(
        "UPDATE users SET password_hash = ? WHERE id = ?",
        (generate_password_hash(new_password), reset_record["user_id"]),
    )
    database.execute(
        "UPDATE password_reset_tokens SET used_at = ? WHERE id = ?",
        (now, reset_record["id"]),
    )
    database.execute("DELETE FROM password_reset_tokens WHERE user_id = ? AND id != ?", (reset_record["user_id"], reset_record["id"]))
    database.commit()
    return True


def list_saved_destinations(user_id):
    rows = get_db().execute(
        """
        SELECT destination_name, created_at FROM saved_destinations
        WHERE user_id = ? ORDER BY created_at DESC
        """,
        (user_id,),
    ).fetchall()
    return [{"destination_name": row["destination_name"], "created_at": row["created_at"]} for row in rows]


def save_destination(user_id, destination_name):
    database = get_db()
    database.execute(
        "INSERT OR IGNORE INTO saved_destinations (user_id, destination_name) VALUES (?, ?)",
        (user_id, destination_name),
    )
    database.commit()


def remove_saved_destination(user_id, destination_name):
    database = get_db()
    cursor = database.execute(
        "DELETE FROM saved_destinations WHERE user_id = ? AND destination_name = ?",
        (user_id, destination_name),
    )
    database.commit()
    return cursor.rowcount > 0
