
"""Tests for the ORVGROUP skill router."""

import pytest

from agent.skill_router import route_task


def test_routes_python_task():
    skills = route_task("Debug a Python error")

    assert "python-debugging" in skills


def test_routes_frontend_task():
    skills = route_task("Build a React website")

    assert "frontend-developer" in skills


def test_routes_git_task():
    skills = route_task("Create a GitHub pull request")

    assert "git-workflow" in skills


def test_rejects_empty_task():
    with pytest.raises(ValueError):
        route_task("")
