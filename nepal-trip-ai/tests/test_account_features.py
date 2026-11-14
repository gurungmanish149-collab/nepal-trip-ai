from urllib.parse import parse_qs, urlparse
from datetime import date, timedelta

from app import create_app


def make_client(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "himalaya-test.sqlite3"),
            "RESET_PASSWORD_DEMO_MODE": True,
        }
    )
    return app.test_client()


def create_account(client, email="traveler@example.com"):
    response = client.post(
        "/api/signup",
        json={
            "fullName": "Test Traveler",
            "username": "testtraveler",
            "email": email,
            "password": "old-password-123",
            "travelInterest": "culture",
        },
        headers=csrf_headers(client),
    )
    assert response.status_code == 201


def csrf_headers(client):
    response = client.get("/api/me")
    return {"X-CSRF-Token": response.get_json()["csrf_token"]}


def test_demo_password_reset_changes_password_and_invalidates_link(tmp_path):
    client = make_client(tmp_path)
    create_account(client)

    request_reset = client.post("/api/password-reset/request", json={"email": "traveler@example.com"})
    assert request_reset.status_code == 200
    reset_url = request_reset.get_json()["demo_reset_url"]
    token = parse_qs(urlparse(reset_url).fragment)["token"][0]

    reset = client.post(
        "/api/password-reset/confirm",
        json={
            "token": token,
            "password": "new-password-456",
            "passwordConfirmation": "new-password-456",
        },
    )
    assert reset.status_code == 200
    assert client.get("/api/me").get_json()["user"] is None

    reused = client.post(
        "/api/password-reset/confirm",
        json={
            "token": token,
            "password": "another-password-789",
            "passwordConfirmation": "another-password-789",
        },
    )
    assert reused.status_code == 400

    client.post("/api/signout", headers=csrf_headers(client))
    sign_in = client.post(
        "/api/signin",
        json={"email": "traveler@example.com", "password": "new-password-456"},
        headers=csrf_headers(client),
    )
    assert sign_in.status_code == 200


def test_wishlist_is_persisted_for_signed_in_user(tmp_path):
    client = make_client(tmp_path)
    create_account(client, "wishlist@example.com")

    save = client.post(
        "/api/wishlist",
        json={"destination": "pokhara lakeside"},
        headers=csrf_headers(client),
    )
    assert save.status_code == 201
    assert save.get_json()["destination"] == "Pokhara Lakeside"

    wishlist = client.get("/api/wishlist")
    assert wishlist.status_code == 200
    assert wishlist.get_json()["items"][0]["destination_name"] == "Pokhara Lakeside"

    remove = client.delete(
        "/api/wishlist",
        json={"destination": "Pokhara Lakeside"},
        headers=csrf_headers(client),
    )
    assert remove.status_code == 200
    assert client.get("/api/wishlist").get_json()["items"] == []


def test_authenticated_writes_require_csrf_token(tmp_path):
    client = make_client(tmp_path)
    signup_without_token = client.post(
        "/api/signup",
        json={
            "fullName": "Test Traveler",
            "username": "csrfuser",
            "email": "csrf@example.com",
            "password": "old-password-123",
            "travelInterest": "culture",
        },
    )
    assert signup_without_token.status_code == 400

    create_account(client, "csrf@example.com")

    response = client.post("/api/wishlist", json={"destination": "Pokhara"})

    assert response.status_code == 400
    assert "token" in response.get_json()["error"].lower()


def test_trip_inquiry_is_saved_and_not_a_confirmed_booking(tmp_path):
    client = make_client(tmp_path)
    create_account(client, "inquiry@example.com")
    departure = (date.today() + timedelta(days=30)).isoformat()
    returning = (date.today() + timedelta(days=35)).isoformat()

    response = client.post(
        "/api/trip-inquiries",
        json={
            "departureCountry": "Japan",
            "destination": "Pokhara",
            "departureDate": departure,
            "returnDate": returning,
        },
        headers=csrf_headers(client),
    )

    assert response.status_code == 201
    assert "not a confirmed booking" in response.get_json()["message"]
    inquiry_id = response.get_json()["inquiry"]["id"]
    saved = client.get("/api/trip-inquiries").get_json()["items"]
    assert saved[0]["id"] == inquiry_id
    assert saved[0]["status"] == "pending"


def test_trip_inquiry_rejects_invalid_dates(tmp_path):
    client = make_client(tmp_path)
    create_account(client, "dates@example.com")
    departure = (date.today() + timedelta(days=3)).isoformat()

    response = client.post(
        "/api/trip-inquiries",
        json={
            "departureCountry": "Japan",
            "destination": "Pokhara",
            "departureDate": departure,
            "returnDate": departure,
        },
        headers=csrf_headers(client),
    )

    assert response.status_code == 400


def test_password_recovery_requests_are_rate_limited(tmp_path):
    client = make_client(tmp_path)
    responses = [
        client.post("/api/password-reset/request", json={"email": "missing@example.com"})
        for _ in range(6)
    ]

    assert [response.status_code for response in responses[:5]] == [200] * 5
    assert responses[5].status_code == 429


def test_failed_signin_attempts_are_rate_limited(tmp_path):
    client = make_client(tmp_path)
    create_account(client, "signin-limit@example.com")
    responses = [
        client.post(
            "/api/signin",
            json={"email": "signin-limit@example.com", "password": "not-the-password"},
            headers=csrf_headers(client),
        )
        for _ in range(11)
    ]

    assert all(response.status_code == 401 for response in responses[:10])
    assert responses[10].status_code == 429
