"""Tests for agent configuration."""

from agent.config import AgentConfig, load_config


def test_default_config():
    config = AgentConfig()

    assert config.model == "gpt-4.1-mini"
    assert config.max_steps == 10
    assert config.require_approval is True


def test_load_config_from_environment(monkeypatch):
    monkeypatch.setenv("ORVGROUP_MODEL", "test-model")
    monkeypatch.setenv("ORVGROUP_MAX_STEPS", "5")
    monkeypatch.setenv("ORVGROUP_REQUIRE_APPROVAL", "false")

    config = load_config()

    assert config.model == "test-model"
    assert config.max_steps == 5
    assert config.require_approval is False
