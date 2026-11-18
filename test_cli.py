"""Tests for the command-line interface."""

import json
import sys
from unittest.mock import patch

import pytest

from agent.cli import main


@patch("agent.cli.run_agent")
def test_cli_prints_agent_result(mock_run_agent, capsys):
    mock_run_agent.return_value = {
        "goal": "Build a website",
        "execution_status": "failed",
    }

    with patch.object(sys, "argv", ["orvgroup-agent", "Build a website"]):
        main()

    output = capsys.readouterr().out
    result = json.loads(output)

    assert result["goal"] == "Build a website"
    assert result["execution_status"] == "failed"


@patch("agent.cli.run_agent")
def test_cli_handles_agent_error(mock_run_agent, capsys):
    mock_run_agent.side_effect = ValueError("Test error")

    with patch.object(sys, "argv", ["orvgroup-agent", "Test task"]):
        with pytest.raises(SystemExit) as error:
            main()

    assert error.value.code == 1
    assert "Agent error: Test error" in capsys.readouterr().out
