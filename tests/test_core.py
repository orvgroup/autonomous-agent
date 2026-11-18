"""Tests for the ORVGROUP agent core."""

from unittest.mock import patch

from agent.core import run_agent


@patch("agent.core.run_task")
@patch("agent.core.generate_response")
@patch("agent.core.get_skills_for_task")
def test_run_agent(
    mock_skills,
    mock_llm,
    mock_run_task,
):
    mock_skills.return_value = ["python-debugging"]
    mock_llm.return_value = "Here is the solution"
    mock_run_task.return_value.status.value = "failed"

    result = run_agent("Debug a Python error")

    assert result["response"] == "Here is the solution"
    assert "python-debugging" in result["selected_skills"]
