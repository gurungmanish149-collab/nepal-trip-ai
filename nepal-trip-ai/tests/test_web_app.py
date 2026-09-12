import os
import subprocess
import sys
import time
import urllib.request
import uuid

from app.web_app import app


def test_script_entrypoint_runs_from_project_root():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env = os.environ.copy()
    env["PYTHONPATH"] = root
    proc = subprocess.Popen([sys.executable, "app/web_app.py"], cwd=root, env=env)

    try:
        deadline = time.time() + 15
        last_error = None
        while time.time() < deadline:
            try:
                with urllib.request.urlopen("http://127.0.0.1:5000/", timeout=2) as response:
                    body = response.read()
                    assert response.status == 200
                    assert b"NepalTrip AI" in body
                    break
            except Exception as exc:  # pragma: no cover - retry loop for startup timing
                last_error = exc
                time.sleep(0.5)
        else:
            raise AssertionError(f"server did not start: {last_error}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


def test_homepage_works():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"NepalTrip AI" in response.data
    assert b"Map View" in response.data


def test_search_form_uses_requested_nepal_filter_labels():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Days" in response.data
    assert b"NPR 150,000" in response.data
    assert b"Select" in response.data
    assert b"Type interests like culture" in response.data
    assert b"Spring" in response.data


def test_planner_route_returns_results():
    client = app.test_client()
    response = client.post(
        "/plan",
        data={
            "days": "5",
            "budget": "450",
            "region": "Any",
            "interests": "culture, food",
            "season": "spring",
        },
    )

    assert response.status_code == 200
    assert b"Kathmandu" in response.data
    assert b"/images/" in response.data


def test_japanese_language_support():
    client = app.test_client()
    response = client.post(
        "/plan",
        data={
            "days": "5",
            "budget": "450",
            "region": "Any",
            "interests": "culture, food",
            "season": "spring",
            "language": "ja",
        },
    )

    assert response.status_code == 200
    assert b"\xe6\x97\x85\xe8\xa1\x8c\xe6\x97\xa5\xe6\x95\xb0" in response.data


def test_region_filter_returns_matches_when_a_specific_region_is_chosen():
    client = app.test_client()
    response = client.post(
        "/plan",
        data={
            "days": "5",
            "budget": "450",
            "region": "Central",
            "interests": "culture, food",
            "season": "spring",
        },
    )

    assert response.status_code == 200
    assert b"Kathmandu" in response.data
    assert b"No destinations match your current filters" not in response.data


def test_blank_region_and_season_selectors_do_not_show_all_destinations():
    client = app.test_client()
    response = client.post(
        "/plan",
        data={
            "days": "5",
            "budget": "450",
            "region": "Select",
            "interests": "culture, food",
            "season": "Select",
        },
    )

    assert response.status_code == 200
    assert b"Please select a region or season" in response.data
    assert b"Found" not in response.data


def test_chinese_and_korean_language_support():
    client = app.test_client()
    response = client.post(
        "/plan",
        data={
            "days": "5",
            "budget": "450",
            "region": "Any",
            "interests": "culture, food",
            "season": "spring",
            "language": "zh",
        },
    )

    assert response.status_code == 200
    assert b"\xe6\x97\x85\xe8\xa1\x8c" in response.data

    response_ko = client.post(
        "/plan",
        data={
            "days": "5",
            "budget": "450",
            "region": "Any",
            "interests": "culture, food",
            "season": "spring",
            "language": "ko",
        },
    )

    assert response_ko.status_code == 200
    assert b"\xec\x97\x85\xec\x97\x85" not in response_ko.data


def test_logged_in_user_can_access_dashboard_page():
    client = app.test_client()
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_name"] = "Test User"

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Test User" in response.data
    assert b"Find my trip" in response.data
    assert b'id="departure-date" type="date" min=""' in response.data
    assert b'id="return-date" type="date" min=""' in response.data


def test_direct_app_signup_api_returns_json():
    client = app.test_client()
    suffix = uuid.uuid4().hex[:8]
    response = client.post(
        "/api/signup",
        json={
            "fullName": "JSON User",
            "username": f"jsonuser_{suffix}",
            "email": f"jsonuser_{suffix}@example.com",
            "password": "password123",
            "travelInterest": "mountains",
        },
    )

    assert response.status_code == 201
    assert response.is_json
    assert "Account created successfully." in response.get_json()["message"]


def test_duplicate_username_is_rejected():
    client = app.test_client()
    suffix = uuid.uuid4().hex[:8]

    first = client.post(
        "/api/signup",
        json={
            "fullName": "Same Name User",
            "username": f"samenameuser_{suffix}",
            "email": f"same-name-1-{suffix}@example.com",
            "password": "password123",
            "travelInterest": "culture",
        },
    )
    assert first.status_code == 201

    second = client.post(
        "/api/signup",
        json={
            "fullName": "Another Same Name User",
            "username": f"samenameuser_{suffix}",
            "email": f"same-name-2-{suffix}@example.com",
            "password": "password123",
            "travelInterest": "wildlife",
        },
    )

    assert second.status_code == 409
    assert "username" in second.get_json()["error"].lower()
