import hashlib
import hmac
import secrets
import sqlite3
import time
from dataclasses import dataclass

from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from .database import get_db


@dataclass
class User:
    id: int
    full_name: str
    username: str
    email: str
    travel_interest: str
    auth_version: int = 0


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
        "SELECT id, full_name, username, email, password_hash, travel_interest, auth_version FROM users WHERE email = ?",
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
    return User(
        user["id"], user["full_name"], user["username"], user["email"],
        user["travel_interest"], user["auth_version"]
    )


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


def revoke_password_reset_tokens(user_id):
    database = get_db()
    database.execute("DELETE FROM password_reset_tokens WHERE user_id = ?", (user_id,))
    database.commit()


def reset_password_with_token(token, new_password):
    if not token:
        return False

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = int(time.time())
    database = get_db()
    try:
        database.execute("BEGIN IMMEDIATE")
        reset_record = database.execute(
            """
            SELECT id, user_id FROM password_reset_tokens
            WHERE token_hash = ? AND used_at IS NULL AND expires_at >= ?
            """,
            (token_hash, now),
        ).fetchone()
        if reset_record is None:
            database.rollback()
            return False

        updated = database.execute(
            """
            UPDATE password_reset_tokens SET used_at = ?
            WHERE id = ? AND used_at IS NULL AND expires_at >= ?
            """,
            (now, reset_record["id"], now),
        )
        if updated.rowcount != 1:
            database.rollback()
            return False

        database.execute(
            "UPDATE users SET password_hash = ?, auth_version = auth_version + 1 WHERE id = ?",
            (generate_password_hash(new_password), reset_record["user_id"]),
        )
        database.execute(
            "DELETE FROM password_reset_tokens WHERE user_id = ? AND id != ?",
            (reset_record["user_id"], reset_record["id"]),
        )
        database.commit()
        return True
    except sqlite3.Error:
        database.rollback()
        raise


def create_trip_inquiry(user_id, departure_country, destination_name, departure_date, return_date):
    database = get_db()
    cursor = database.execute(
        """
        INSERT INTO trip_inquiries
            (user_id, departure_country, destination_name, departure_date, return_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, departure_country, destination_name, departure_date, return_date),
    )
    database.commit()
    return cursor.lastrowid


def list_trip_inquiries(user_id):
    rows = get_db().execute(
        """
        SELECT id, departure_country, destination_name, departure_date, return_date, status, created_at
        FROM trip_inquiries WHERE user_id = ? ORDER BY created_at DESC, id DESC
        """,
        (user_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def rate_limit_exceeded(scope, identity, limit, window_seconds):
    """Persist a privacy-preserving fixed-window counter across app workers."""
    now = int(time.time())
    bucket_hash = hmac.new(
        str(current_app.secret_key).encode("utf-8"),
        f"{scope}:{identity}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    database = get_db()
    try:
        database.execute("BEGIN IMMEDIATE")
        row = database.execute(
            "SELECT window_started_at, attempts FROM request_rate_limits WHERE bucket_hash = ?",
            (bucket_hash,),
        ).fetchone()
        if row is None or now - row["window_started_at"] >= window_seconds:
            database.execute(
                """
                INSERT INTO request_rate_limits (bucket_hash, window_started_at, attempts)
                VALUES (?, ?, 1)
                ON CONFLICT(bucket_hash) DO UPDATE SET
                    window_started_at = excluded.window_started_at,
                    attempts = 1
                """,
                (bucket_hash, now),
            )
            attempts = 1
        else:
            attempts = row["attempts"] + 1
            database.execute(
                "UPDATE request_rate_limits SET attempts = ? WHERE bucket_hash = ?",
                (attempts, bucket_hash),
            )
        database.execute(
            "DELETE FROM request_rate_limits WHERE window_started_at < ?",
            (now - 86400,),
        )
        database.commit()
        return attempts > limit
    except sqlite3.Error:
        database.rollback()
        raise


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
