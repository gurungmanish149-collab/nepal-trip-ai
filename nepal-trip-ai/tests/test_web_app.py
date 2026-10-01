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
    )
    assert response.status_code == 201, response.get_json()
    return response.get_json()["user"]


def test_homepage_and_signin_pages_load(client):
    assert client.get("/").status_code == 200
    assert b"<span class=\"brand-mark\">G</span>" in client.get("/").data
    assert client.get("/signin.html").status_code == 200
    assert client.get("/signup.html").status_code == 200


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
            "season": "",
        },
    )
    assert response.status_code == 200
    assert b"$400" in response.data
    assert b"$1,400" in response.data
    assert b"$1,800" in response.data
    assert b"/dashboard/images/pokhara_image.jpg" in response.data


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
    first = client.post("/api/signup", json=payload)
    assert first.status_code == 201
    duplicate = dict(payload, email=f"another-{suffix}@example.com")
    second = client.post("/api/signup", json=duplicate)
    assert second.status_code == 409
    assert "username" in second.get_json()["error"].lower()
