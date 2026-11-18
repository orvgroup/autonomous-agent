
"""Tests for the ORVGROUP AI Agent web application."""

from fastapi.testclient import TestClient

from webapp.main import app

client = TestClient(app)


def test_homepage_returns_html():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "ORVGROUP AI Agent" in response.text


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_requires_login():
    response = client.post(
        "/api/chat",
        json={"prompt": "Build a website"},
    )

    assert response.status_code == 401


def test_login_and_chat(monkeypatch):
    monkeypatch.setenv("APP_USERNAME", "testuser")
    monkeypatch.setenv("APP_PASSWORD", "testpassword")

    def fake_run_agent(prompt):
        return {
            "goal": prompt,
            "execution_status": "failed",
        }

    monkeypatch.setattr(
        "webapp.main.run_agent",
        fake_run_agent,
    )

    with TestClient(app) as authenticated_client:
        login_response = authenticated_client.post(
            "/api/login",
            json={
                "username": "testuser",
                "password": "testpassword",
            },
        )

        assert login_response.status_code == 200

        response = authenticated_client.post(
            "/api/chat",
            json={"prompt": "Build a website"},
        )

        assert response.status_code == 200
        assert response.json()["goal"] == "Build a website"


def test_login_rejects_wrong_password(monkeypatch):
    monkeypatch.setenv("APP_USERNAME", "testuser")
    monkeypatch.setenv("APP_PASSWORD", "testpassword")

    response = client.post(
        "/api/login",
        json={
            "username": "testuser",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_chat_rejects_empty_prompt():
    response = client.post(
        "/api/chat",
        json={"prompt": ""},
    )

    assert response.status_code == 422
