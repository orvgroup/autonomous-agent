
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


def test_chat_endpoint_returns_agent_result(monkeypatch):
    def fake_run_agent(prompt):
        return {
            "goal": prompt,
            "execution_status": "failed",
        }

    monkeypatch.setattr(
        "webapp.main.run_agent",
        fake_run_agent,
    )

    response = client.post(
        "/api/chat",
        json={"prompt": "Build a website"},
    )

    assert response.status_code == 200
    assert response.json()["goal"] == "Build a website"


def test_chat_rejects_empty_prompt():
    response = client.post(
        "/api/chat",
        json={"prompt": ""},
    )

    assert response.status_code == 422
