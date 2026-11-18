"""Tests for the ORVGROUP LLM integration."""

from unittest.mock import MagicMock, patch

import pytest

from agent.llm import generate_response


def test_rejects_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        generate_response("Hello")


def test_rejects_empty_prompt(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    with pytest.raises(ValueError):
        generate_response("   ")


@patch("agent.llm.OpenAI")
def test_generates_response(mock_openai, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_response = MagicMock()
    mock_response.output_text = "Hello from ORVGROUP Agent"

    mock_client.responses.create.return_value = mock_response

    result = generate_response("Say hello")

    assert result == "Hello from ORVGROUP Agent"
    mock_client.responses.create.assert_called_once()
