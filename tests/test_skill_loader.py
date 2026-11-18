"""Tests for the skill loader."""

from unittest.mock import patch

from agent.skill_loader import load_skill


@patch("agent.skill_loader.urlopen")
def test_load_skill_returns_content(mock_urlopen):
    mock_response = mock_urlopen.return_value.__enter__.return_value
    mock_response.read.return_value = (
        b"# Python Debugging\n\nDebugging instructions."
    )

    result = load_skill("python-debugging")

    assert "Python Debugging" in result
    assert "Debugging instructions" in result


def test_load_skill_rejects_unknown_skill():
    import pytest

    with pytest.raises(ValueError):
        load_skill("unknown-skill")
        
from agent.skill_loader import list_skills


def test_list_skills_returns_available_skills():
    skills = list_skills()

    assert "python-debugging" in skills
    assert "frontend-developer" in skills
    assert "code-reviewer" in skills
    assert len(skills) == 6
