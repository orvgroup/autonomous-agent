
"""Tests for the ORVGROUP task planner."""

import pytest

from agent.models import TaskStatus
from agent.planner import create_plan


def test_create_plan_with_valid_goal():
    plan = create_plan("Build a Python API")

    assert plan.goal == "Build a Python API"
    assert len(plan.steps) == 5
    assert plan.status == TaskStatus.PENDING


def test_create_plan_rejects_empty_goal():
    with pytest.raises(ValueError):
        create_plan("")


def test_create_plan_rejects_whitespace_goal():
    with pytest.raises(ValueError):
        create_plan("   ")
