import re

from flask import Blueprint, current_app, jsonify, request, session, send_from_directory

from .models import authenticate_user, create_user, find_user_by_email


pages = Blueprint("pages", __name__)
auth_api = Blueprint("auth_api", __name__)
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ALLOWED_INTERESTS = {"mountains", "culture", "wildlife", "slow"}


def serve_page(filename):
    return send_from_directory(current_app.config["PROJECT_ROOT"], filename)


@pages.get("/")
def home():
    return serve_page("index.html")


@pages.get("/signin.html")
def signin_page():
    return serve_page("signin.html")


@pages.get("/signup.html")
def signup_page():
    return serve_page("signup.html")


@pages.get("/<path:filename>")
def public_file(filename):
    return send_from_directory(current_app.config["PROJECT_ROOT"], filename)


def validate_signup(payload):
    full_name = payload.get("fullName", "").strip()
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")
    travel_interest = payload.get("travelInterest", "")

    if not full_name:
        return None, "Please enter your name."
    if not EMAIL_PATTERN.match(email):
        return None, "Please enter a valid email address."
    if len(password) < 8:
        return None, "Your password must be at least 8 characters."
    if travel_interest not in ALLOWED_INTERESTS:
        return None, "Please choose a travel style."
    return (full_name, email, password, travel_interest), None


@auth_api.post("/signup")
def signup():
    payload = request.get_json(silent=True) or request.form
    values, error = validate_signup(payload)
    if error:
        return jsonify({"error": error}), 400

    full_name, email, password, travel_interest = values
    if find_user_by_email(email) is not None:
        return jsonify({"error": "An account with that email already exists."}), 409

    user = create_user(full_name, email, password, travel_interest)
    session.clear()
    session["user_id"] = user.id
    session["user_name"] = user.full_name
    return jsonify({"message": "Account created successfully.", "user": {"name": user.full_name, "email": user.email}}), 201


@auth_api.post("/signin")
def signin():
    payload = request.get_json(silent=True) or request.form
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")
    user = authenticate_user(email, password)
    if user is None:
        return jsonify({"error": "Email or password is incorrect."}), 401

    session.clear()
    session["user_id"] = user.id
    session["user_name"] = user.full_name
    return jsonify({"message": f"Welcome back, {user.full_name}.", "user": {"name": user.full_name, "email": user.email}})


@auth_api.post("/signout")
def signout():
    session.clear()
    return jsonify({"message": "You have been signed out."})


@auth_api.get("/me")
def current_user():
    if "user_id" not in session:
        return jsonify({"user": None})
    return jsonify({"user": {"id": session["user_id"], "name": session["user_name"]}})
