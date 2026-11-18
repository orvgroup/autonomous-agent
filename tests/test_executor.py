
"""Tests for the ORVGROUP execution engine."""

from agent.executor import run_task
from agent.models import TaskStatus


def test_run_task_completes_plan():
    plan = run_task("Build a Python API")

    assert plan.status == TaskStatus.COMPLETED
    assert len(plan.steps) == 5


def test_run_task_completes_all_steps():
    plan = run_task("Review a project")

    for step in plan.steps:
        assert step.status == TaskStatus.COMPLETED


def test_run_task_preserves_goal():
    goal = "Create a website"
    plan = run_task(goal)

    assert plan.goal == goal
