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
