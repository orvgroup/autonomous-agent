
"""Execution engine for the ORVGROUP autonomous agent."""

from agent.models import TaskPlan, TaskStatus
from agent.planner import create_plan


def execute_plan(plan: TaskPlan) -> TaskPlan:
    """Report execution honestly until action handlers are connected."""

    if not plan.steps:
        plan.status = TaskStatus.FAILED
        return plan

    plan.status = TaskStatus.IN_PROGRESS

    for step in plan.steps:
        step.status = TaskStatus.FAILED
        step.result = (
            "Execution is not implemented yet. "
            "No action was performed."
        )

    plan.status = TaskStatus.FAILED
    return plan


def run_task(goal: str) -> TaskPlan:
    """Create and process a task plan."""

    plan = create_plan(goal)
    return execute_plan(plan)
