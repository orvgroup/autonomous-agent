"""Additional tests for planner validation."""

import pytest

from agent.planner import create_plan


def test_create_plan_rejects_empty_goal():
    with pytest.raises(ValueError):
        create_plan("")


def test_create_plan_rejects_whitespace_goal():
    with pytest.raises(ValueError):
        create_plan("   ")


def test_create_plan_creates_five_steps():
    plan = create_plan("Build a website")

    assert plan.goal == "Build a website"
    assert len(plan.steps) == 5
