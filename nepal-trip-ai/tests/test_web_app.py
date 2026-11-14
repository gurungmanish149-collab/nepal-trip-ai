from datetime import date, timedelta
import uuid

import pytest

from app import create_app
from app.web_app import DESTINATION_CATALOG, NEPAL_PLACES


@pytest.fixture

def app(tmp_path):
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "DATABASE": str(tmp_path / "test.sqlite3"),
        }
    )


@pytest.fixture

def client(app):
    return app.test_client()


def create_account(client):
    suffix = uuid.uuid4().hex[:8]
    response = client.post(
        "/api/signup",
        json={
            "fullName": "Test User",
            "username": f"testuser_{suffix}",
            "email": f"test-{suffix}@example.com",
            "password": "password123",
            "travelInterest": "mountains",
        },
        headers=csrf_headers(client),
    )
    assert response.status_code == 201, response.get_json()
    return response.get_json()["user"]


def csrf_headers(client):
    response = client.get("/api/me")
    return {"X-CSRF-Token": response.get_json()["csrf_token"]}


def test_homepage_and_signin_pages_load(client):
    assert client.get("/").status_code == 200
    assert b"<span class=\"brand-mark\">G</span>" in client.get("/").data
    assert client.get("/signin.html").status_code == 200
    assert client.get("/signup.html").status_code == 200
    response = client.get("/styles.css")
    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_private_project_files_are_not_served_as_public_assets(client):
    assert client.get("/app/database.py").status_code == 404
    assert client.get("/instance/himalaya.sqlite3").status_code == 404
    assert client.get("/README.md").status_code == 404


def test_production_requires_configured_secret_key(monkeypatch):
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.delenv("SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app()


def test_dashboard_requires_login_and_legacy_route_redirects(client):
    assert client.get("/dashboard/").status_code == 302
    create_account(client)
    response = client.get("/dashboard")
    assert response.status_code == 308
    assert response.headers["Location"].endswith("/dashboard/")
    assert client.get("/dashboard/").status_code == 200


def test_dashboard_has_country_and_all_destination_options_without_budget_or_map(client):
    create_account(client)
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert all(country.encode() in response.data for country in ("Japan", "America", "Australia", "China", "Korea", "Mongolia", "UK"))
    assert all(place["name"].encode() in response.data for place in DESTINATION_CATALOG)
    assert b'name="budget"' not in response.data
    assert b"Map View" not in response.data
    assert b"Leaflet" not in response.data
    assert b'id="trip-inquiry-form"' in response.data
    assert b'id="planner-inquiry-list"' in response.data
    assert b'name="csrf_token"' in response.data
    assert response.data.count('class="planner-required">[必須]</span>'.encode()) == 5
    assert all(f"Step {step}".encode() in response.data for step in range(1, 6))
    assert all(text.encode() in response.data for text in ("Country（国）", "Destination（目的地）", "Departure date（出発日）", "Return date（帰国日）", "Season（旅行シーズン）"))
    assert b'id="destination-preview-season"' in response.data
    assert b'id="season" name="season" required' in response.data
    assert b"countrySelect.addEventListener('change', clearAfterCountry)" in response.data
    assert b"seasonSelect.addEventListener('change'" in response.data


def test_destination_images_are_available():
    client
    app = create_app({"TESTING": True, "DATABASE": ":memory:"})
    test_client = app.test_client()
    assert all(test_client.get(place["image"]).status_code == 200 for place in NEPAL_PLACES)
    assert all(test_client.get(place["image_url"]).status_code == 200 for place in DESTINATION_CATALOG)


def test_search_calculates_local_cost_and_airfare_without_budget_input(client):
    create_account(client)
    departure = (date.today() + timedelta(days=1)).isoformat()
    returned = (date.today() + timedelta(days=6)).isoformat()
    response = client.post(
        "/dashboard/plan",
        data={
            "country": "America",
            "destination": "Pokhara",
            "depart_date": departure,
            "return_date": returned,
            "season": "spring",
        },
    )
    assert response.status_code == 200
    assert b"$400" in response.data
    assert b"$1,400" in response.data
    assert b"$1,800" in response.data
    assert b"/dashboard/images/pokhara_image.jpg" in response.data


def test_planner_requires_each_step_in_order_and_accepts_any_season(client):
    create_account(client)
    departure = (date.today() + timedelta(days=1)).isoformat()
    returned = (date.today() + timedelta(days=6)).isoformat()
    complete_payload = {
        "country": "America",
        "destination": "Pokhara",
        "depart_date": departure,
        "return_date": returned,
        "season": "spring",
    }
    missing_steps = (
        ("country", "Please choose a country."),
        ("destination", "Please choose a Nepal destination."),
        ("depart_date", "Please choose a departure date."),
        ("return_date", "Please choose a return date after the departure date."),
        ("season", "Please choose a season."),
    )
    for field, expected_message in missing_steps:
        incomplete_payload = {**complete_payload, field: ""}
        response = client.post("/dashboard/plan", data=incomplete_payload)
        assert expected_message.encode() in response.data

    invalid_return = client.post(
        "/dashboard/plan",
        data={**complete_payload, "return_date": departure},
    )
    assert b"Please enter valid travel dates." in invalid_return.data

    any_season = client.post("/dashboard/plan", data={**complete_payload, "season": "any"})
    assert any_season.status_code == 200
    assert b"Destination matched your trip." in any_season.data


def test_language_switch_preserves_selected_search_values(client):
    create_account(client)
    departure = (date.today() + timedelta(days=1)).isoformat()
    returned = (date.today() + timedelta(days=6)).isoformat()
    response = client.get(
        "/dashboard/plan",
        query_string={
            "lang": "ja",
            "country": "America",
            "destination": "Pokhara",
            "depart_date": departure,
            "return_date": returned,
            "season": "",
        },
    )
    assert response.status_code == 200
    assert "出発国".encode() in response.data
    assert "Pokhara".encode() in response.data
    assert "旅行費用の目安".encode() in response.data


def test_departure_date_in_the_past_is_rejected(client):
    create_account(client)
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    response = client.post(
        "/dashboard/plan",
        data={
            "country": "America",
            "destination": "Pokhara",
            "depart_date": yesterday,
            "return_date": date.today().isoformat(),
            "season": "",
        },
    )
    assert "Departure date cannot be in the past.".encode() in response.data


def test_direct_signup_api_requires_unique_username(client):
    suffix = uuid.uuid4().hex[:8]
    payload = {
        "fullName": "JSON User",
        "username": f"jsonuser_{suffix}",
        "email": f"jsonuser_{suffix}@example.com",
        "password": "password123",
        "travelInterest": "mountains",
    }
    first = client.post("/api/signup", json=payload, headers=csrf_headers(client))
    assert first.status_code == 201
    duplicate = dict(payload, email=f"another-{suffix}@example.com")
    second = client.post("/api/signup", json=duplicate, headers=csrf_headers(client))
    assert second.status_code == 409
    assert "username" in second.get_json()["error"].lower()
