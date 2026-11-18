
"""Tests for the ORVGROUP execution engine."""

from agent.executor import run_task
from agent.models import TaskStatus


def test_run_task_does_not_claim_false_completion():
    plan = run_task("Build a Python API")

    assert plan.status == TaskStatus.FAILED
    assert len(plan.steps) == 5


def test_run_task_marks_unimplemented_steps_failed():
    plan = run_task("Review a project")

    for step in plan.steps:
        assert step.status == TaskStatus.FAILED
        assert "No action was performed." in step.result


def test_run_task_preserves_goal():
    goal = "Create a website"
    plan = run_task(goal)

    assert plan.goal == goal
