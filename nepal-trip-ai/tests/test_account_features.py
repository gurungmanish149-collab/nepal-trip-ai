from urllib.parse import parse_qs, urlparse

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
    )
    assert response.status_code == 201


def test_demo_password_reset_changes_password_and_invalidates_link(tmp_path):
    client = make_client(tmp_path)
    create_account(client)

    request_reset = client.post("/api/password-reset/request", json={"email": "traveler@example.com"})
    assert request_reset.status_code == 200
    reset_url = request_reset.get_json()["demo_reset_url"]
    token = parse_qs(urlparse(reset_url).query)["token"][0]

    reset = client.post(
        "/api/password-reset/confirm",
        json={
            "token": token,
            "password": "new-password-456",
            "passwordConfirmation": "new-password-456",
        },
    )
    assert reset.status_code == 200

    reused = client.post(
        "/api/password-reset/confirm",
        json={
            "token": token,
            "password": "another-password-789",
            "passwordConfirmation": "another-password-789",
        },
    )
    assert reused.status_code == 400

    client.post("/api/signout")
    sign_in = client.post("/api/signin", json={"email": "traveler@example.com", "password": "new-password-456"})
    assert sign_in.status_code == 200


def test_wishlist_is_persisted_for_signed_in_user(tmp_path):
    client = make_client(tmp_path)
    create_account(client, "wishlist@example.com")

    save = client.post("/api/wishlist", json={"destination": "pokhara lakeside"})
    assert save.status_code == 201
    assert save.get_json()["destination"] == "Pokhara Lakeside"

    wishlist = client.get("/api/wishlist")
    assert wishlist.status_code == 200
    assert wishlist.get_json()["items"][0]["destination_name"] == "Pokhara Lakeside"

    remove = client.delete("/api/wishlist", json={"destination": "Pokhara Lakeside"})
    assert remove.status_code == 200
    assert client.get("/api/wishlist").get_json()["items"] == []
